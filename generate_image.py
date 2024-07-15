from PIL import Image, ImageDraw, ImageFont
import os

def generate_image(username):
    print(f"Generating image for username: {username}")

    # Create an image with white background
    img = Image.new('RGB', (200, 100), color = (255, 255, 255))
    
    # Initialize ImageDraw
    d = ImageDraw.Draw(img)
    
    # Load a font
    fnt = ImageFont.load_default()
    
    # Position of the text
    text_position = (10, 40)
    
    # Draw the text on the image
    d.text(text_position, username, font=fnt, fill=(0, 0, 0))
    
    # Save the image
    if not os.path.exists('images'):
        os.makedirs('images')
    image_path = os.path.join('images', f"{username}.jpg")
    img.save(image_path)
    print(f"Image saved to {image_path}")

# Example usage
if __name__ == "__main__":
    generate_image("example_username")
