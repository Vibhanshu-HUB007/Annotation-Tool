# Implementation Notes

## WSI Tile Source Implementation

The current implementation uses a custom tile source function for OpenSeadragon. For production use, consider:

1. **DeepZoom Format**: Pre-generate DeepZoom pyramids using `vips` or similar tools
2. **IIIF Format**: Implement IIIF Image API 2.1 or 3.0 for standardized tile serving
3. **Tile Caching**: Implement server-side tile caching to improve performance
4. **Background Processing**: Use Celery or similar for async tile generation

## Annotation Drawing Implementation

The current annotation overlay uses Fabric.js for rendering. For full annotation drawing capabilities, you'll need to:

1. **Implement Drawing Tools**: Add mouse event handlers to capture drawing paths
2. **Coordinate Transformation**: Convert viewport coordinates to WSI coordinates
3. **Geometry Creation**: Convert drawing paths to GeoJSON format
4. **Real-time Preview**: Show annotation preview while drawing

## AI Integration

The AI endpoints are currently placeholders. To implement:

1. **Model Loading**: Load PyTorch/ONNX models in the backend
2. **Tile Extraction**: Extract tiles from WSI for inference
3. **Inference Pipeline**: Run model inference on tiles
4. **Post-processing**: Convert predictions to annotation format
5. **Active Learning**: Store corrections for model retraining

## Performance Optimizations

1. **Tile Pre-generation**: Pre-generate tiles for faster loading
2. **CDN**: Use CDN for tile serving
3. **Web Workers**: Use Web Workers for annotation processing
4. **Virtual Scrolling**: Implement virtual scrolling for annotation lists

## Security Considerations

1. **File Upload Validation**: Add virus scanning for uploaded files
2. **Rate Limiting**: Implement rate limiting on API endpoints
3. **Input Sanitization**: Sanitize all user inputs
4. **HTTPS**: Use HTTPS in production
5. **Token Refresh**: Implement token refresh mechanism

## Database Migrations

Use Alembic for database migrations:

```bash
alembic init alembic
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

## Testing

Add comprehensive tests:

1. **Unit Tests**: Test individual functions and components
2. **Integration Tests**: Test API endpoints
3. **E2E Tests**: Test full user workflows
4. **Performance Tests**: Test with large WSI files

## Deployment Checklist

- [ ] Set `DEBUG=False` in production
- [ ] Configure PostgreSQL database
- [ ] Set secure `SECRET_KEY`
- [ ] Configure CORS for production domain
- [ ] Set up SSL/TLS certificates
- [ ] Configure file storage (S3, etc.)
- [ ] Set up monitoring and logging
- [ ] Configure backup strategy
- [ ] Set up CI/CD pipeline
