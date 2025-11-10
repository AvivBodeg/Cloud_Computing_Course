# Service for handling picture downloads, storage, and serving
#
# Responsibilities:
# - Download images from URLs provided in pet creation/updates
# - Store images in local files with unique names
# - Serve images via GET /pictures/{file-name}
# - Handle different image formats (JPEG, PNG)
# - Clean up image files when pets are deleted