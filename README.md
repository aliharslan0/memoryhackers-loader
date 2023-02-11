# memoryhackers-loader

## Kullanım
`.env` dosyasındaki MDATA[^1], B64[^2] ve ID[^3] boşluklarını doldurun, `pip install -r requirements.txt` komutunu çalıştırın ve son olarak `main.py` dosyasını çalıştırın.

## Açıklama
Bir hilenin B64 ve ID değerlerine sahipseniz, çalışıyor durumda gözükmese bile çalışacaktır. Ancak, "güncelleniyor" veya "çalışmıyor" durumunda olan hileleri bu yöntemle çalıştırmak hileyi güncellemeyecek veya çalışır hale getirmeyecektir. Bu script sadece, bir saat için kullanıcı arayüzünü kullanmadan hileyi çalıştırmanızı sağlar. Ayrıca, B64 ve ID kodlarına sahip olmanız durumunda, erişiminiz olmayan hilelerin çalışıp çalışmayacağı kesin değildir.

## Örnek
https://user-images.githubusercontent.com/97433474/218171547-2151ca5f-07c2-4e1e-9316-4e4e8b999bfa.mp4

[^1]: ![mdata](https://user-images.githubusercontent.com/97433474/218167255-022c6baf-dc37-4cd4-93e2-6cbff35706c2.png)
[^2]: ![resim](https://user-images.githubusercontent.com/97433474/218167527-70fcd935-0da8-4ef9-a3d9-40a8a77a43e0.png) rdCheat fonksiyonunun ilk parametresi.
[^3]: rdCheat fonksiyonunun ikinci parametresi.
