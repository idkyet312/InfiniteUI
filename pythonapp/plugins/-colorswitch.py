from PIL import Image

def change_background_color(image_path, new_color, save_path):
    # Load the image
    image = Image.open(image_path).convert("RGBA")
    
    # Assuming the original background is of a specific color we want to replace
    # We create a new image with the same data but replace the background color
    data = image.getdata()
    new_data = []
    for item in data:
        # Change background color (example uses white background) to dark green
        if item[:3] == (255, 255, 255):  # Checking if the pixel is white
            new_data.append(new_color + (255,))  # New color with full opacity
        else:
            new_data.append(item)  # Original data

    image.putdata(new_data)
    image.save(save_path)

# Example usage - replace 'path_to_your_herbivore.png' and 'path_to_your_carnivore.png' with actual paths
change_background_color('herbivore.png', (0, 100, 0), 'herbivore2.png')
change_background_color('carnivore.png', (0, 100, 0), 'carnivore2.png')