# Kompresja plików

## Kompresja

> [!NOTE]
> skompresowane słowa mają stałą długość w bitach

- pierwszy bajt -> długość słownika (n)

- kolejne n bajtów -> elementy słownika

- kolejne 3 bity (values: 0-7) -> ile bitów na końcu pliku doppisaliśmy aby ilośc bitów po kompresji była wielokrotnością 8

- `skompresowany tekst`

- dopisane bity (0-7)
