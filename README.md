# Backend for BetterCovers-frontend

## Endpoints:  
/imageCache/<base64>  
Downloads the image from the url encoded in base64 and returns it, subsequent requests will be server from local cache.

/api/getImage?<parameters>  
Returns a BetterCovers image with the parameters requested

/static/<file>  
Serves static files from BetterCovers/config
