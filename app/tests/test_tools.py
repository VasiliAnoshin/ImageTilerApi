import pytest
from unittest.mock import MagicMock
import sys
import os
from pathlib import Path
sys.path.append(Path(__file__).parents[2].as_posix())
sys.path.append(Path(__file__).parents[3].as_posix())
from app.tools import Tools

@pytest.fixture
def tools():
    return Tools()

def test_generate_image_id(tools):
    # Create a mock for the logger
    logger = MagicMock()

    # Set the mock logger for the Tools class
    Tools.logger = logger

    # Perform the test
    user_id = "12345"
    image_id = Tools.genrate_image_id(user_id)

    # Assertions
    assert user_id in image_id

def test_allowed_file(tools):
    # Test case for allowed file with a valid file name
    assert tools.allowed_file("image.jpg") is True

    # Test case for allowed file with an invalid file name
    assert tools.allowed_file("image.txt") is False

def test_is_valid_tiles_format(tools):
    # Test case for valid tiles format
    assert tools.is_valid_tiles_format("256x256") is True

    # Test case for invalid tiles format
    assert tools.is_valid_tiles_format("abc") is False

def test_get_current_directory(tools):
    # Test case for valid input
    user_id = "12345"
    image_id = "image123"
    tiles = "256x256"
    expected_directory = f"{os.getcwd()}\\app\\Data\\{user_id}\\{image_id}\\{tiles} tiles"
    assert tools.get_current_directory(user_id, image_id, tiles) == expected_directory

    # Test case for empty user_id
    with pytest.raises(ValueError):
        tools.get_current_directory("", image_id, tiles)

    # Test case for empty image_id
    with pytest.raises(ValueError):
        tools.get_current_directory(user_id, "", tiles)

    # Test case for empty tiles
    with pytest.raises(ValueError):
        tools.get_current_directory(user_id, image_id, "")

    # Test case for invalid tiles format
    with pytest.raises(Exception):
        tools.get_current_directory(user_id, image_id, "abc")
    
def test_generate_image_id_with_different_user_ids(tools):
    # Create a mock for the logger
    logger = MagicMock()

    # Set the mock logger for the Tools class
    Tools.logger = logger

    # Perform the test with different user IDs
    user_id_1 = "user1"
    image_id_1 = Tools.genrate_image_id(user_id_1)

    user_id_2 = "user2"
    image_id_2 = Tools.genrate_image_id(user_id_2)

    # Assertions
    assert user_id_1 in image_id_1
    assert user_id_2 in image_id_2


def test_allowed_file_with_different_file_extensions(tools):
    # Test case for allowed file with different extensions
    assert tools.allowed_file("image.jpg") is True
    assert tools.allowed_file("image.jpeg") is True
    assert tools.allowed_file("image.png") is True
    assert tools.allowed_file("image.txt") is False
    assert tools.allowed_file("image.pdf") is False


def test_is_valid_tiles_format_with_different_formats(tools):
    # Test case for valid tiles formats
    assert tools.is_valid_tiles_format("256x256") is True
    assert tools.is_valid_tiles_format("512x512") is True
    assert tools.is_valid_tiles_format("1024x1024") is True

    # Test case for invalid tiles formats
    assert tools.is_valid_tiles_format("abc") is False
    assert tools.is_valid_tiles_format("256x") is False
    assert tools.is_valid_tiles_format("x256") is False
    assert tools.is_valid_tiles_format("256*256") is False


def test_get_current_directory_with_different_input(tools):
    # Test case for valid input
    user_id = "user1"
    image_id = "image1"
    tiles = "256x256"
    expected_directory = f"{os.getcwd()}\\app\\Data\\{user_id}\\{image_id}\\{tiles} tiles"
    assert tools.get_current_directory(user_id, image_id, tiles) == expected_directory

    # Test case for empty user_id
    with pytest.raises(ValueError):
        tools.get_current_directory("", image_id, tiles)

    # Test case for empty image_id
    with pytest.raises(ValueError):
        tools.get_current_directory(user_id, "", tiles)

    # Test case for empty tiles
    with pytest.raises(ValueError):
        tools.get_current_directory(user_id, image_id, "")

    # Test case for invalid tiles format
    with pytest.raises(Exception):
        tools.get_current_directory(user_id, image_id, "abc")