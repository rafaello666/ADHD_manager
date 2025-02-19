<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <title>Galeria Obrazów</title>
    <style>
        body {
            font-family: Arial, sans-serif;
        }
        .gallery {
            display: flex;
            flex-wrap: wrap;
        }
        .image-container {
            margin: 10px;
            text-align: center;
        }
        .image-container img {
            max-width: 200px;
            height: auto;
            display: block;
            margin-bottom: 5px;
        }
        .image-container a {
            text-decoration: none;
            color: #000;
        }
    </style>
</head>
<body>
    <h1>Galeria Obrazów</h1>
    <div class="gallery">
        <?php
            // Lista dozwolonych rozszerzeń plików graficznych
            $allowed_extensions = array("jpg", "jpeg", "png", "gif", "bmp", "webp");

            // Pobierz wszystkie pliki z bieżącego katalogu
            $files = scandir(__DIR__);

            foreach ($files as $file) {
                // Pobierz rozszerzenie pliku
                $file_extension = strtolower(pathinfo($file, PATHINFO_EXTENSION));

                // Sprawdź, czy plik jest obrazem
                if (in_array($file_extension, $allowed_extensions)) {
                    // Pobierz pełną ścieżkę do pliku
                    $file_url = htmlspecialchars($file);

                    // Wyświetl obraz, nazwę pliku i link do URL
                    echo '<div class="image-container">';
                    echo '<a href="' . $file_url . '" target="_blank">';
                    echo '<img src="' . $file_url . '" alt="' . htmlspecialchars($file) . '">';
                    echo '</a>';
                    echo '<div>' . htmlspecialchars($file) . '</div>';
                    echo '<div><a href="' . $file_url . '" target="_blank">Link do obrazu</a></div>';
                    echo '</div>';
                }
            }
        ?>
    </div>
</body>
</html>
