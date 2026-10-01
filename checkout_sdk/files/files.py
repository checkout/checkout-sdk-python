class FileRequest:
    """A file to upload to the Files API (POST /files), sent as a multipart request. The returned ID
    is what document front and back attributes take."""
    # The path to the file to upload (JPEG, PNG or PDF).
    # [Required]
    file: str
    # The purpose of the file upload. For onboarding documents, one of the FilePurpose values from
    # checkout_sdk.accounts.accounts (for example 'identity_verification'); for disputes,
    # 'dispute_evidence'.
    # [Required]
    purpose: str
