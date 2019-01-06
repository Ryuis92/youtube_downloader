# -*- coding: utf-8 -*-
"""Applies in-place data mutations."""
from __future__ import absolute_import

import json
import logging
import pprint

from pytube import cipher
from pytube.compat import parse_qsl
from pytube.compat import unquote
from pytube.exceptions import LiveStreamError


logger = logging.getLogger(__name__)


def apply_signature(config_args, fmt, js):
    """Apply the decrypted signature to the stream manifest.

    :param dict config_args:
        Details of the media streams available.
    :param str fmt:
        Key in stream manifests (``ytplayer_config``) containing progressive
        download or adaptive streams (e.g.: ``url_encoded_fmt_stream_map`` or
        ``adaptive_fmts``).
    :param str js:
        The contents of the base.js asset file.

    """
    stream_manifest = config_args[fmt]
    live_stream = json.loads(config_args['player_response']).get(
        'playabilityStatus', {},
    ).get('liveStreamability')
    for i, stream in enumerate(stream_manifest):                       ## key point
        if 'url' in stream:
            url = stream['url']
        elif live_stream:                                              ## check if this video url is streamed right now, which you cannot download
            raise LiveStreamError('Video is currently being streamed live')

        if 'signature=' in url:
            # For certain videos, YouTube will just provide them pre-signed, in
            # which case there's no real magic to download them and we can skip
            # the whole signature descrambling entirely.
            logger.debug('signature found, skip decipher')
            continue

        if js is not None:
            signature = cipher.get_signature(js, stream['s'])
        else:
            # signature not present in url (line 33), need js to descramble
            # TypeError caught in __main__
            raise TypeError('JS is None')

        logger.debug(
            'finished descrambling signature for itag=%s\n%s',
            stream['itag'], pprint.pformat(
                {
                    's': stream['s'],
                    'signature': signature,
                }, indent=2,
            ),
        )
        stream_manifest[i]['url'] = url + '&signature=' + signature


def apply_descrambler(stream_data, key):
    """Apply various in-place transforms to YouTube's media stream data.

    Creates a ``list`` of dictionaries by string splitting on commas, then
    taking each list item, parsing it as a query string, converting it to a
    ``dict`` and unquoting the value.

    :param dict stream_data:
        Dictionary containing query string encoded values.
    :param str key:
        Name of the key in dictionary.

    **Example**:

    >>> d = {'foo': 'bar=1&var=test,em=5&t=url%20encoded'}
    >>> apply_descrambler(d, 'foo')
    >>> print(d)
    {'foo': [{'bar': '1', 'var': 'test'}, {'em': '5', 't': 'url encoded'}]}
    
    1.get stream_data which is like d in this example.
    2.transform value of stream_data[key] to the form of list of dicts
    """
    stream_data[key] = [
        {k: unquote(v) for k, v in parse_qsl(i)}        ## 2. then for each i do parse_qsl(i) to make a (key, val) tuple
        for i in stream_data[key].split(',')            ## 1. this line works first. split string in stream_data[key] on comma and make it list
    ]
    

    logger.debug(
        'applying descrambler\n%s',
        pprint.pformat(stream_data[key], indent=2),
    )
