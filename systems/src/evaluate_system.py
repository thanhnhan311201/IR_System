from system import CBIR_System

if __name__ == '__main__':
    dataset_path = 'systems/datasets/oxbuild_dataset/'
    image_folder = 'IRsystem_WebPage/static/datasets/oxbuild_dataset/images/'

    my_system = CBIR_System(dataset_path, image_folder)

    my_system.evaluate_system()