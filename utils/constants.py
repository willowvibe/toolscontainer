
format_to_codec = {
    ".mp4": ["libx264", "libx265"],  # H.264 and HEVC
    ".avi": ["mpeg4", "xvid"],  # Common AVI codecs
    ".mov": ["libx264", "h263", "mpeg4"],  # Various codecs used in MOV
    ".mkv": ["libx264", "libvpx-vp9", "libtheora"],  # Common codecs for MKV
    ".flv": ["flv"],  # FLV has a single primary codec
    ".wmv": ["wmv2", "wmv3"],  # Windows Media codecs
    ".webm": ["libvpx-vp9", "libvpx-vp8"],  # VP8 and VP9 for WebM
    ".ogv": ["libtheora"],  # Primary codec for Ogg Video
    ".gif": ["gif"],  # GIF has a single format

    # Additional formats and codecs
    ".mpg": ["mpeg1", "mpeg2"],  # MPEG-1 and MPEG-2 for MPG
    ".ts": ["h264", "h265"],  # H.264 and HEVC for Transport Stream
    ".3gp": ["mpeg4", "h263"],  # Common codecs for 3GP
    ".aac": ["aac"],  # Audio-only AAC
    ".flac": ["flac"],  # Audio-only FLAC
    ".mp3": ["liblame"],  # Common MP3 encoder
    ".ogg": ["libvorbis"],  # Audio-only Ogg Vorbis
}

video_formats = {
    '.mp4': ['libx264', 'aac'],
    '.mkv': ['libx265', 'aac'],
    '.mov': ['libx264', 'aac'],
    '.avi': ['mpeg4', 'mp3'],
    '.wmv': ['wmv2', 'wmav2']
}


audio_formats = {
    '.mp3': ['mp3'],
    '.wav': ['pcm_s16le'],
    '.flac': ['flac'],
    '.aac': ['aac'],
    '.ogg': ['libvorbis'],
    '.wma': ['wmav2']
}
