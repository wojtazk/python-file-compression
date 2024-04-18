# Kompresja plików

## Kompresja

> [!NOTE]
> skompresowane słowa mają stałą długość w bitach

- pierwszy bajt -> długość słownika (n)

- kolejne n bajtów -> elementy słownika

- kolejne 3 bity (values: 0-7) -> ile bitów na końcu pliku doppisaliśmy aby ilośc bitów po kompresji była wielokrotnością 8

- `skompresowany tekst`

- dopisane bity (0-7)

## Użycie

### Help

```
python compressor.py --help
```
```
usage: compressor.py [-h] [-d] [--details] input_file output_file

Program for compressing and decompressing files

positional arguments:
input_file
output_file

options:
-h, --help        show this help message and exit
-d, --decompress  Decompress data in input_file and save it to output_file
--details         Print detailed information about compression / decompression
```

### Kompresja

```
python compressor.py input_file compressed_file
```

### Dekompresja


```
python compressor.py -d compressed_file decompressed_file
```
