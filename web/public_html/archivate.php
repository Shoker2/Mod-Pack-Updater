<?php
function archivate_folder($folder_path, $zip_file) {
    if (file_exists($zip_file)) {
        unlink($zip_file);
    }
    touch($zip_file);

    $zip = new ZipArchive;
    $this_zip = $zip->open($zip_file);

    if ($this_zip) {
        $files = new RecursiveIteratorIterator(
            new RecursiveDirectoryIterator($folder_path),
            RecursiveIteratorIterator::LEAVES_ONLY
        );

        foreach ($files as $file)
        {
            if (!$file->isDir())
            {
                $relativePath = substr($file, strlen($folder_path) + 1);

                $zip->addFile($file, $relativePath);
            }
        }

        $zip ->close(); 
    }
}

set_time_limit(300);
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

$files = scandir("./Modpacks");

foreach ($files as $file) {
    if ($file != '.' && $file != '..') {
        archivate_folder("./Modpacks/" . $file, "./Resourses/" . $file . ".zip");
    }
}

?>