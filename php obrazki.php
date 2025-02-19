<?php
// Pobierz listę plików w bieżącym folderze
$files = array_diff(scandir(__DIR__), array('.', '..'));

// Filtruj tylko pliki graficzne
$imageExtensions = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp'];
$images = array_filter($files, function($file) use ($imageExtensions) {
    $extension = pathinfo($file, PATHINFO_EXTENSION);
    return in_array(strtolower($extension), $imageExtensions);
});
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Image Gallery</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            background-color: #f0f0f0;
        }
        .image-container {
            margin: 10px;
            border: 2px solid #ccc;
            border-radius: 5px;
            overflow: hidden;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            text-align: center;
            background-color: #fff;
        }
        img {
            max-width: 100%;
            height: auto;
            display: block;
        }
        a {
            display: block;
            margin: 5px 0;
            color: #0066cc;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <?php if (!empty($images)): ?>
        <?php foreach ($images as $image): ?>
            <div class="image-container">
                <img src="<?php echo $image; ?>" alt="<?php echo $image; ?>">
                <a href="<?php echo $image; ?>" target="_blank">
                    <?php echo $image; ?>
                </a>
            </div>
        <?php endforeach; ?>
    <?php else: ?>
        <p>No images found in the current folder.</p>
    <?php endif; ?>
</body>
</html>
