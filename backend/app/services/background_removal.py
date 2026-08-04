"""
Background removal service using rembg.
"""
import io
from PIL import Image
from rembg import remove, new_session


class BackgroundRemovalService:
    """Service for removing backgrounds from product images."""
    
    def __init__(self):
        # Use u2net model - good balance of speed and quality
        self.session = new_session("u2net")
    
    def remove_background(
        self,
        image: Image.Image,
        alpha_matting: bool = False,
        alpha_matting_foreground_threshold: int = 240,
        alpha_matting_background_threshold: int = 10,
    ) -> Image.Image:
        """
        Remove background from an image.
        
        Args:
            image: Input PIL Image
            alpha_matting: Use alpha matting for better edges
            alpha_matting_foreground_threshold: Foreground threshold
            alpha_matting_background_threshold: Background threshold
            
        Returns:
            PIL Image with transparent background
        """
        # Convert to bytes
        img_bytes = io.BytesIO()
        image.save(img_bytes, format="PNG")
        img_bytes.seek(0)
        
        # Remove background
        output_bytes = remove(
            img_bytes.read(),
            session=self.session,
            alpha_matting=alpha_matting,
            alpha_matting_foreground_threshold=alpha_matting_foreground_threshold,
            alpha_matting_background_threshold=alpha_matting_background_threshold,
        )
        
        # Convert back to PIL Image
        return Image.open(io.BytesIO(output_bytes))
    
    def remove_background_with_mask(
        self,
        image: Image.Image,
    ) -> tuple[Image.Image, Image.Image]:
        """
        Remove background and return both the result and the mask.
        
        Args:
            image: Input PIL Image
            
        Returns:
            Tuple of (image with transparent bg, binary mask)
        """
        result = self.remove_background(image)
        
        # Extract alpha channel as mask
        if result.mode == "RGBA":
            mask = result.split()[3]
        else:
            mask = Image.new("L", result.size, 255)
        
        return result, mask


# Singleton instance
_service: BackgroundRemovalService | None = None


def get_background_removal_service() -> BackgroundRemovalService:
    """Get or create the background removal service."""
    global _service
    if _service is None:
        _service = BackgroundRemovalService()
    return _service
