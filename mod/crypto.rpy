init -998 python in _fom_autosave_crypto:
    import ctypes
    import hashlib
    import os

    import _ssl
    _lib = ctypes.CDLL(_ssl.__file__)

    # EVP GCM control codes
    _GCM_SET_IVLEN = 0x9
    _GCM_GET_TAG   = 0x10
    _GCM_SET_TAG   = 0x11

    IV_LEN  = 12  # bytes, standard GCM nonce
    TAG_LEN = 16  # bytes, GCM authentication tag
    KEY_LEN = 32  # bytes, AES-256

    # ctypes signatures
    _lib.EVP_CIPHER_CTX_new.restype  = ctypes.c_void_p
    _lib.EVP_CIPHER_CTX_new.argtypes = []

    _lib.EVP_CIPHER_CTX_free.restype  = None
    _lib.EVP_CIPHER_CTX_free.argtypes = [ctypes.c_void_p]

    _lib.EVP_aes_256_gcm.restype  = ctypes.c_void_p
    _lib.EVP_aes_256_gcm.argtypes = []

    _lib.EVP_EncryptInit_ex.restype  = ctypes.c_int
    _lib.EVP_EncryptInit_ex.argtypes = [ctypes.c_void_p, ctypes.c_void_p,
                                        ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p]

    _lib.EVP_EncryptUpdate.restype  = ctypes.c_int
    _lib.EVP_EncryptUpdate.argtypes = [ctypes.c_void_p, ctypes.c_char_p,
                                       ctypes.POINTER(ctypes.c_int), ctypes.c_char_p, ctypes.c_int]

    _lib.EVP_EncryptFinal_ex.restype  = ctypes.c_int
    _lib.EVP_EncryptFinal_ex.argtypes = [ctypes.c_void_p, ctypes.c_char_p,
                                         ctypes.POINTER(ctypes.c_int)]

    _lib.EVP_DecryptInit_ex.restype  = ctypes.c_int
    _lib.EVP_DecryptInit_ex.argtypes = [ctypes.c_void_p, ctypes.c_void_p,
                                        ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p]

    _lib.EVP_DecryptUpdate.restype  = ctypes.c_int
    _lib.EVP_DecryptUpdate.argtypes = [ctypes.c_void_p, ctypes.c_char_p,
                                       ctypes.POINTER(ctypes.c_int), ctypes.c_char_p, ctypes.c_int]

    _lib.EVP_DecryptFinal_ex.restype  = ctypes.c_int
    _lib.EVP_DecryptFinal_ex.argtypes = [ctypes.c_void_p, ctypes.c_char_p,
                                         ctypes.POINTER(ctypes.c_int)]

    _lib.EVP_CIPHER_CTX_ctrl.restype  = ctypes.c_int
    _lib.EVP_CIPHER_CTX_ctrl.argtypes = [ctypes.c_void_p, ctypes.c_int,
                                         ctypes.c_int, ctypes.c_void_p]

    def _check(rv, label):
        if rv <= 0:
            raise RuntimeError("OpenSSL call failed: {0} (rv={1})".format(label, rv))

    def _to_bytes(s):
        if isinstance(s, unicode):
            return s.encode("utf-8")
        return s

    def derive_key(seed_phrase):
        """Derive a 32-byte AES-256 key from a seed phrase via PBKDF2-HMAC-SHA256."""
        return hashlib.pbkdf2_hmac(b"sha256", _to_bytes(seed_phrase), b"fom-autosave-v1", 100000, KEY_LEN)

    def derive_user_id(seed_phrase):
        """Derive the server-side user identifier (SHA-512 hex) from a seed phrase."""
        return hashlib.sha512(_to_bytes(seed_phrase)).hexdigest()

    def encrypt(plaintext, key):
        """
        Encrypt plaintext with AES-256-GCM.
        Returns bytes in the format: IV (12) || tag (16) || ciphertext.
        The IV is randomly generated per call.
        """

        plaintext = _to_bytes(plaintext)
        iv        = os.urandom(IV_LEN)

        ctx = _lib.EVP_CIPHER_CTX_new()
        if not ctx:
            raise RuntimeError("EVP_CIPHER_CTX_new failed")

        try:
            cipher = _lib.EVP_aes_256_gcm()
            _check(_lib.EVP_EncryptInit_ex(ctx, cipher, None, None, None), "EncryptInit cipher")
            _check(_lib.EVP_CIPHER_CTX_ctrl(ctx, _GCM_SET_IVLEN, IV_LEN, None), "GCM_SET_IVLEN")
            _check(_lib.EVP_EncryptInit_ex(ctx, None, None, key, iv), "EncryptInit key+iv")

            buf     = ctypes.create_string_buffer(len(plaintext) + 16)
            buf_len = ctypes.c_int(0)
            _check(_lib.EVP_EncryptUpdate(ctx, buf, ctypes.byref(buf_len), plaintext, len(plaintext)), "EncryptUpdate")
            ciphertext = buf.raw[:buf_len.value]

            fin     = ctypes.create_string_buffer(16)
            fin_len = ctypes.c_int(0)
            _check(_lib.EVP_EncryptFinal_ex(ctx, fin, ctypes.byref(fin_len)), "EncryptFinal")
            ciphertext += fin.raw[:fin_len.value]

            tag = ctypes.create_string_buffer(TAG_LEN)
            _check(_lib.EVP_CIPHER_CTX_ctrl(ctx, _GCM_GET_TAG, TAG_LEN, tag), "GCM_GET_TAG")
            return iv + tag.raw + ciphertext

        finally:
            _lib.EVP_CIPHER_CTX_free(ctx)

    def decrypt(data, key):
        """
        Decrypt data produced by encrypt().
        Expects bytes in the format: IV (12) || tag (16) || ciphertext.
        Raises RuntimeError if authentication fails (wrong key or tampered data).
        """

        if len(data) < IV_LEN + TAG_LEN:
            raise ValueError("Data too short to be a valid ciphertext")

        iv         = data[:IV_LEN]
        tag        = data[IV_LEN:IV_LEN + TAG_LEN]
        ciphertext = data[IV_LEN + TAG_LEN:]

        ctx = _lib.EVP_CIPHER_CTX_new()
        if not ctx:
            raise RuntimeError("EVP_CIPHER_CTX_new failed")
        try:
            cipher = _lib.EVP_aes_256_gcm()
            _check(_lib.EVP_DecryptInit_ex(ctx, cipher, None, None, None), "DecryptInit cipher")
            _check(_lib.EVP_CIPHER_CTX_ctrl(ctx, _GCM_SET_IVLEN, IV_LEN, None),  "GCM_SET_IVLEN")
            _check(_lib.EVP_DecryptInit_ex(ctx, None, None, key, iv),             "DecryptInit key+iv")

            buf     = ctypes.create_string_buffer(len(ciphertext) + 16)
            buf_len = ctypes.c_int(0)
            _check(_lib.EVP_DecryptUpdate(ctx, buf, ctypes.byref(buf_len), ciphertext, len(ciphertext)), "DecryptUpdate")
            plaintext = buf.raw[:buf_len.value]

            tag_buf = ctypes.create_string_buffer(tag, TAG_LEN)
            _check(_lib.EVP_CIPHER_CTX_ctrl(ctx, _GCM_SET_TAG, TAG_LEN, tag_buf), "GCM_SET_TAG")

            fin     = ctypes.create_string_buffer(16)
            fin_len = ctypes.c_int(0)
            if _lib.EVP_DecryptFinal_ex(ctx, fin, ctypes.byref(fin_len)) <= 0:
                raise RuntimeError("Decryption failed: authentication tag mismatch")

            plaintext += fin.raw[:fin_len.value]
            return plaintext

        finally:
            _lib.EVP_CIPHER_CTX_free(ctx)
