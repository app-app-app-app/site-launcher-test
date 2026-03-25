<!doctype html>
<html lang="en-HK">

<head>
    <meta name="referrer" content="no-referrer">
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Glückwünsche!</title>
    <link rel="stylesheet" href="thx/thx.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/parallax/3.1.0/parallax.min.js"></script>

    <?php
    $pfb = isset($_GET['pfb']) ? $_GET['pfb'] : '';
    $click_id = isset($_GET['click_id']) ? $_GET['click_id'] : '';
    $redirect_url = isset($_GET['redirect_url']) ? $_GET['redirect_url'] : '';
    $language = isset($_GET['language']) ? $_GET['language'] : '';
    ?>

    <!-- fb pixel  -->
    <img height="1" width="1" src="https://www.facebook.com/tr?id=<?= $pfb; ?>&ev=Lead&noscript=1&eid=<?= $click_id; ?>" />

    <!-- redirect to autologin url after 3 seconds -->
    <script>
        const redirectUrl = '<?= $redirect_url; ?>';

        if (redirectUrl !== null && redirectUrl !== '') {
            setTimeout(function() {
                window.location.href = redirectUrl;
            }, 3000);
        }
    </script>
</head>

<body>
    <div class="thx">
        <div class="thx__container">
            <div class="thx__box">
                <h2 class="thx-left__title">Gratulujemy pomyślnej rejestracji w systemie.</h2>
                <div class="thx-right">
                    <div id="parallax">
                        <div data-depth="0.2" class="thx-right__item-1">
                            <img src="thx/1.png" alt="Congrats item">
                        </div>
                        <div data-depth="0.3" class="thx-right__item-2">
                            <img src="thx/2.png" alt="Congrats item">
                        </div>
                        <div data-depth="0.4" class="thx-right__item-2">
                            <img src="thx/3.png" alt="Congrats item">
                        </div>
                    </div>
                </div>
                <div class="thx-left">
                    <p style="font-size: 16px;" class="thx-left__text">
                        Otrzymasz telefon w ciągu 24 godzin - nie przegap go, <br> w przeciwnym razie możesz zainteresować innego uczestnika!
                    </p>
                </div>
            </div>
        </div>
    </div>
    <script>
        let scene = document.getElementById('parallax');
        let parallaxInstance = new Parallax(scene);
    </script>

    <script>
        let language = '<?= $language; ?>';

        const translations = {
            en: {
                title: "Congratulations on your successful registration in the system.",
                text: "You will receive a call within 24 hours - don't miss it, otherwise you might be interesting for another subscriber!"
            },
            de: {
                title: "Herzlichen Glückwunsch zur erfolgreichen Registrierung im System.",
                text: "Sie erhalten innerhalb von 24 Stunden einen Anruf - verpassen Sie ihn nicht, sonst könnte es für einen anderen Abonnenten interessant sein!"
            },
            ru: {
                title: "Поздравляем с успешной регистрацией в системе.",
                text: "Вы получите звонок в течение 24 часов - не пропустите его, иначе вы можете заинтересовать другого абонента!"
            },
            it: {
                title: "Congratulazioni per la tua registrazione avvenuta con successo nel sistema.",
                text: "Riceverai una chiamata entro 24 ore - non perderla, altrimenti potresti essere interessante per un altro abbonato!"
            },
            tr: {
                title: "Sisteme başarılı kaydınızdan dolayı tebrikler.",
                text: "24 saat içinde bir arama alacaksınız - kaçırmayın, aksi takdirde başka bir abone için ilginç olabilirsiniz!"
            },
            pt: {
                title: "Enhorabuena por su registro.",
                text: "En un plazo de 24 horas recibirá una llamada: ¡no la pierda, de lo contrario puede interesar a otro abonado!"
            },
            pl: {
                title: "Gratulacje z okazji pomyślnej rejestracji w systemie.",
                text: "Otrzymasz telefon w ciągu 24 godzin - nie przegap go, w przeciwnym razie możesz być interesujący dla innego abonenta!"
            },
            hu: {
                title: "Gratulálok a sikeres regisztrációhoz a rendszerben.",
                text: "24 órán belül fog kapni egy hívást - ne hagyja ki, különben egy másik előfizető számára is érdekes lehet!"
            },
            ro: {
                title: "Felicitări pentru înregistrarea dvs. reușită în sistem.",
                text: "Veți primi un apel în termen de 24 de ore - nu-l ratați, altfel puteți fi interesant pentru un alt abonat!"
            },
            ae: {
                title: "تهانينا على تسجيلك الناجح في النظام.",
                text: "ستتلقى مكالمة في غضون 24 ساعة - لا تفوتها، وإلا فقد تكون مثيرة للاهتمام بالنسبة لمشترك آخر!"
            },
            jp: {
                title: "システムへのご成功登録おめでとうございます。",
                text: "24時間以内にお電話を差し上げますので、お見逃しなく。それ以外の場合、他の加入者にとって興味深いかもしれません！"
            },
            br: {
                title: "Parabéns pelo seu registro bem-sucedido no sistema.",
                text: "Você receberá uma ligação dentro de 24 horas - não perca, caso contrário, você pode ser interessante para outro assinante!"
            },
            ca: {
                title: "Congratulations on your successful registration in the system.",
                text: "You will receive a call within 24 hours - don't miss it, otherwise you might be interesting for another subscriber!"
            },
            sg: {
                title: "Sistemde başarılı kaydınız için tebrikler.",
                text: "24 saat içinde bir çağrı alacaksınız - kaçırmayın, aksi takdirde başka bir abone için ilginç olabilirsiniz!"
            },
            hk: {
                title: "系統中的成功註冊，恭喜.",
                text: "您將在24小時內收到一通電話 - 請勿錯過，否則您可能對其他訂閱者有興趣！"
            },
            in: {
                title: "सिस्टम में आपके सफल पंजीकरण के लिए बधाई.",
                text: "आपको 24 घंटे के भीतर एक कॉल मिलेगा - इसे मत छोड़िए, अन्यथा आपके लिए कोई और सदस्य रोमांचक हो सकता है!"
            },
            mx: {
                title: "Felicidades por su exitoso registro en el sistema.",
                text: "Recibirá una llamada dentro de las 24 horas. No la pierda, de lo contrario podría ser interesante para otro suscriptor."
            },
            pe: {
                title: "Felicitaciones por su exitoso registro en el sistema.",
                text: "Recibirá una llamada dentro de las 24 horas. No la pierda, de lo contrario podría ser interesante para otro suscriptor."
            },
            cl: {
                title: "Felicitaciones por su exitoso registro en el sistema.",
                text: "Recibirá una llamada dentro de las 24 horas. No la pierda, de lo contrario podría ser interesante para otro suscriptor."
            },
            gb: {
                title: "Congratulations on your successful registration in the system.",
                text: "You will receive a call within 24 hours - don't miss it, otherwise you might be interesting for another subscriber!"
            },
            cs: {
                title: "Gratulujeme k úspěšné registraci do systému.",
                text: "Do 24 hodin obdržíte hovor – nenechte si jej ujít, jinak byste mohli být zajímaví pro dalšího předplatitele!"
            },
        };

        function applyTranslation(lang) {
            const translation = translations[lang] || translations['en'];
            document.querySelector('.thx-left__title').textContent = translation.title;
            document.querySelector('.thx-left__text').innerHTML = translation.text;
            document.title = translation.title;
        }

        window.addEventListener('DOMContentLoaded', () => {
            applyTranslation(language);
        });
    </script>

</body>

</html>