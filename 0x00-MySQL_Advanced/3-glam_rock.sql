-- lists all bands with Glam rock as their main style, ranked by their longevity
SELECT 
    name AS band_name,
    IFNULL(
        (IF(split IS NULL OR split = 0, 2022, split) - formed),
        0
    ) AS lifespan
FROM 
    metal_bands
WHERE 
    genre = 'Glam rock'
ORDER BY 
    lifespan DESC, band_name ASC;
