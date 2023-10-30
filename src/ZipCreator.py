import os
import zipfile
import subprocess
import platform
import sys


def create_requirements_file():
    result = subprocess.run(['pipreqs', '.', '--force'], capture_output=True, text=True)
    if result.returncode == 0:
        print('requirements.txt created successfully')
    else:
        print('Failed to create requirements.txt:', result.stderr, file=sys.stderr)
        sys.exit(result.returncode)


def add_to_zip(zipf, item, base_folder="", prefix="", bad_filenames=None):
    if bad_filenames is None:
        bad_filenames = []

    if os.path.isdir(item):
        for root, dirs, files in os.walk(item):
            if any(badname in root for badname in bad_filenames):
                continue
            for file in files:
                file_path = os.path.join(root, file)
                arcname = prefix + os.path.relpath(file_path, base_folder)
                zipf.write(file_path, arcname)
    elif os.path.isfile(item) and all(badname not in item for badname in bad_filenames):
        arcname = prefix + item
        zipf.write(item, arcname)


def zip_files(output_filename: str, assignment: str, prefix, bad_filenames, *args: str) -> None:
    with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add files and directories
        for item in args:
            prefix = "python_code/"
            add_to_zip(zipf, item, base_folder="", prefix=prefix, bad_filenames=bad_filenames)

        # Add requirements.txt
        zipf.write('requirements.txt', prefix + 'requirements.txt')

        # Add empty folders for input and output of Python Code
        for folder in ["input", "output"]:
            folder_path = f"{prefix}{folder}/{assignment}/"
            zip_info = zipfile.ZipInfo(folder_path)
            zipf.writestr(zip_info, '')

        # output
        output_folder = f'output/{assignment}/'
        add_to_zip(zipf, output_folder, base_folder=output_folder)


def open_folder_in_explorer(folder_path: str) -> None:
    system = platform.system()
    if system == "Windows":
        os.startfile(folder_path)
    elif system == "Darwin":  # macOS
        subprocess.run(["open", folder_path])
    else:  # Linux
        subprocess.run(["xdg-open", folder_path])


if __name__ == "__main__":
    ASSIGNMENT = "Assignment_1"
    output_zip = f'upload/Hess_{ASSIGNMENT}.zip'
    PREFIX = "python/"
    BADFILENAMES = ['__pycache__', 'ZipCreator.py']

    # Create requirements.txt
    create_requirements_file()

    # Create zip file
    zip_files(
        output_zip,
        ASSIGNMENT,
        PREFIX,
        BADFILENAMES,
        'main.py',
        'assignmentconfig.py'
        'src'
    )

    # Open the directory in Explorer
    output_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'upload')
    open_folder_in_explorer(output_folder)
