import os
from typing import Optional, Tuple
from exif import Image
from pathlib import Path
from geopy.geocoders import Nominatim


def fetch_image_size(image_path: Path) -> Optional[int]:
    "Returns image size in bytes"
    size = None
    if image_path.exists():
        size = image_path.stat().st_size
    return size


def fetch_original_image_creation_date(image_path: Path) -> Optional[str]:
    "Returns original image creation data in YYYY:MM:DD HH:MM:SS string format"
    img = Image(image_path)
    return getattr(img, "datetime_original", None)


def fetch_image_format(image_path: Path) -> Optional[str]:
    "Returns extension of image like .jpg, .png etc"
    if image_path.exists:
        return image_path.suffix


def fetch_lat_long_reference_info(image_path: Path) -> Optional[Tuple[str, str]]:
    """
    Get latitude, longitude and reference in the following format
    latitude = 12° 55' 8.472" N
    longitude = 77° 35' 7.668" E
    """
    with open(image_path, "rb") as f:
        img = Image(f)  # Assuming using a library like PIL or exif

    latitude, longitude = None, None

    # Check for existence before accessing attributes
    if hasattr(img, "gps_latitude") and hasattr(img, "gps_latitude_ref"):
        latitude_data = img.gps_latitude
        if latitude_data:
            latitude = f"{latitude_data[0]}° {latitude_data[1]}' {latitude_data[2]:.2f}\" {img.gps_latitude_ref}"

    if hasattr(img, "gps_longitude") and hasattr(img, "gps_longitude_ref"):
        longitude_data = img.gps_longitude
        if longitude_data:
            longitude = f"{longitude_data[0]}° {longitude_data[1]}' {longitude_data[2]:.2f}\" {img.gps_longitude_ref}"

    return latitude, longitude


def parse_lat_long(lat_long_str: str) -> Tuple[float, float, float, str]:
    """
    Extracts degrees, minutes, seconds, and direction from a formatted string.

    Args:
        lat_long_str (str): The latitude or longitude string (e.g., '12.0° 55.0\' 8.47" N')

    Returns:
        Tuple[float, float, float, str]: A tuple containing degrees, minutes, seconds, and direction.
    """
    try:
        parts = lat_long_str.split("°")
        degrees = float(parts[0])
        minutes_seconds = parts[1].split("'")
        minutes = float(minutes_seconds[0])
        seconds = float(minutes_seconds[1].split('"')[0])
        direction = minutes_seconds[1].split('"')[1]
        return degrees, minutes, seconds, direction
    except (IndexError, ValueError):
        raise ValueError("Invalid latitude/longitude format")


def convert_to_decimal_degrees(
    degrees: float, minutes: float, seconds: float, direction: str
) -> float:
    """
    Converts degrees, minutes, seconds with direction to decimal degrees.

    Args:
        degrees (float): Degrees value
        minutes (float): Minutes value
        seconds (float): Seconds value
        direction (str): Direction (N, S, E, W)

    Returns:
        float: The decimal representation of the latitude or longitude.
    """
    decimal_degrees = degrees + minutes / 60 + seconds / 3600
    if direction in ["S", "W"]:
        decimal_degrees *= -1
    return decimal_degrees


def fetch_location_from_lat_long(latitude: str, longitude: str) -> Optional[str]:
    """
    Attempts to convert latitude and longitude with directions into an address using geocoding.

    Args:
        latitude (str): Latitude in degrees, minutes, seconds with direction (e.g., '12.0° 55.0\' 8.47" N')
        longitude (str): Longitude in degrees, minutes, seconds with direction (e.g., '77.0° 35.0\' 7.67" E')

    Returns:
        str: The address corresponding to the given lat-long or None if geocoding fails.
    """

    # Extract degrees, minutes, seconds, and direction
    try:
        lat_deg, lat_min, lat_sec, lat_dir = parse_lat_long(latitude)
        lon_deg, lon_min, lon_sec, lon_dir = parse_lat_long(longitude)
    except ValueError:
        return None

    # Convert to decimal degrees
    latitude_decimal = convert_to_decimal_degrees(lat_deg, lat_min, lat_sec, lat_dir)
    longitude_decimal = convert_to_decimal_degrees(lon_deg, lon_min, lon_sec, lon_dir)

    # Use geocoder to get the address
    try:
        geoLoc = Nominatim(user_agent="GetLoc")
        location = geoLoc.reverse(f"{latitude_decimal},{longitude_decimal}")
        if location.address:
            return location.address
    except Exception as e:
        print(f"Error occured: {e}")
    return None


def fetch_image_captured_location(image_path: Path) -> Optional[str]:
    "Fetches location of the image"
    latitude, longitude = fetch_lat_long_reference_info(image_path)
    if latitude and longitude:
        location = fetch_location_from_lat_long(latitude, longitude)
        return location


def fetch_image_metadata(image_path: Path) -> Optional[dict]:
    """
    Function to extract following meta information of a image
    - image_size in bytes
    - image_format
    - lat_lon
    - location
    """
    return {
        "image_size": fetch_image_size(image_path),
        "image_format": fetch_image_format(image_path),
        "lat_lon": fetch_lat_long_reference_info(image_path),
        "location": fetch_image_captured_location(image_path),
    }
