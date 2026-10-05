class FileRequest:
    """A file to upload to the Files API (POST /files), sent as a multipart request. The returned ID
    is what document front and back attributes take."""
    # The path to the file to upload (JPEG, PNG or PDF).
    # [Required]
    file: str
    # The purpose of the file upload. For onboarding documents, one of the FilePurpose values from
    # checkout_sdk.accounts.accounts (for example 'identity_verification'); for disputes,
    # 'dispute_evidence'.
    # AccountsClient.upload_file sends this request to POST /files on the Files host, which the API
    # reference does not describe. The reference's POST /files is the disputes upload on the API host
    # (DisputesClient.upload_file), whose purpose mentions only dispute_evidence and
    # arbitration_evidence. The onboarding values are the PlatformsFileUpload purposes the reference
    # lists for the sub-entity upload, POST /entities/{entity_id}/files (FilePurpose).
    # [Required]
    purpose: str
