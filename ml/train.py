from tensorflow.keras.preprocessing.image import ImageDataGenerator

IMG_SIZE = (224,224)

datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2
)

train_generator = datagen.flow_from_directory(
    "../dataset/train",
    target_size=IMG_SIZE,
    batch_size=32,
    class_mode="categorical",
    subset="training"
)

validation_generator = datagen.flow_from_directory(
    "../dataset/train",
    target_size=IMG_SIZE,
    batch_size=32,
    class_mode="categorical",
    subset="validation"
)

print(train_generator.class_indices)