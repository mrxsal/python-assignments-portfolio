import os
import pytest
import PIL
from ..filter_image import \
    parse_args, \
    process_image, \
    make_grayscale, \
    add_overlay, \
    rotate, \
    save_image


# TODO: HOW TO AVOID FAILED TESTS FROM CHANGING / ADDING FILES TO PROJECT_FOLDER?

def test_entrypoint():
    exit_status = os.system('python filter_image.py --help')
    assert exit_status == 0


class TestProgram:
    """
    tests the parse_args() function
    """
    def test_parse_args_SimpleCorrect(self):
        """
        Test correct simple command.
        Each filter used once.
        python filter_image.py --gray_scale --rotate -45 --overlay python.png input.jpg output.png
        """
        args = parse_args(['--gray_scale', '--rotate', '-45', '--overlay', 'tests/test_files/python.png', 'tests/test_files/input.jpg', 'tests/test_files/output/test_parse_args_SimpleCorrect.png'])
        process_image(args)
        assert args.input_image == 'tests/test_files/input.jpg'
        assert args.output_image == 'tests/test_files/output/test_parse_args_SimpleCorrect.png'
        assert args.gray_scale is True
        assert args.rotate == [-45]
        assert args.overlay == ['tests/test_files/python.png']

class testProcessImage:
    def test_process_image_InputFileDoesNotExist(self):
        with pytest.raises(FileNotFoundError):
            args = parse_args(['tests/test_files/InputFileDoesNotExist.jpg',
                               'tests/test_files/output/test_parse_args_SimpleCorrect.png'])
            process_image(args)

    def test_process_image_InputFileIsNotAnImage(self):
        with pytest.raises(PIL.UnidentifiedImageError):
            args = parse_args(['requirements.txt',
                               'tests/test_files/output/test_parse_args_SimpleCorrect.png'])
            process_image(args)

class TestFilters:
    def test_make_grayscale_CorrectOutput(self):
        correct_image = PIL.Image.open('tests/test_files/expected_output/test_make_grayscale_CorrectOutput.png')
        input_image = PIL.Image.open('input.jpg')
        processed_image = make_grayscale(input_image)
        assert list(correct_image.getdata()) == list(processed_image.getdata())

    def test_add_overlay_CorrectOutput(self):
        correct_image = PIL.Image.open('tests/test_files/expected_output/test_add_overlay_CorrectOutput.png')
        input_image = PIL.Image.open('input.jpg')
        overlay_image = 'tests/test_files/example_overlay.png'
        processed_image = add_overlay(input_image, overlay_image)
        assert list(correct_image.getdata()) == list(processed_image.getdata())

    def test_rotate_CorrectOutput(self):
        correct_image = PIL.Image.open('tests/test_files/expected_output/test_rotate_CorrectOutput.png')
        input_image = PIL.Image.open('input.jpg')
        processed_image = rotate(input_image, 45)
        assert list(correct_image.getdata()) == list(processed_image.getdata())

class TestSaveImage:
    def test_process_image_IncorrectOutputExtension(self):
        """
        Tests that ValueError is raised when output_image is not a .jpg or .png file.
        """
        with pytest.raises(ValueError):
            image = PIL.Image.open('input.jpg')
            save_image(image, 'test_process_image_IncorrectOutputExtension.abc')

