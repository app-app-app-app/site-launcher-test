<?php
session_start();
if (empty($_SESSION['js_token'])) {
    $_SESSION['js_token'] = bin2hex(random_bytes(16));
}
$jsToken = $_SESSION['js_token'];

require_once 'offer_seo.php';
include 'lang.php';
?>
<?php
if (strpos($_SERVER['HTTP_HOST'], 'www.') === 0) {
    $host = substr($_SERVER['HTTP_HOST'], 4);
    header("Location: https://" . $host . $_SERVER['REQUEST_URI'], true, 301);
    exit();
}
?>
<!DOCTYPE html>
<html lang="<?= $site_lang ?>">

<head>
<?php
$host = $_SERVER['HTTP_HOST'];
$uri = strtok($_SERVER['REQUEST_URI'], '?'); // без GET-параметрів

$canonical = 'https://' . $host . $uri;
?>

<link rel="canonical" href="<?= htmlspecialchars($canonical, ENT_QUOTES, 'UTF-8'); ?>" />

  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">

<script type="application/ld+json">
{
  "@context": "https://schema.org/",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "<?= $site_name ?>",
      "item": "<?= $site_url ?>"
    },
    {
      "@type": "ListItem",
      "position": 2,
      "name": "⚡ <?= $site_name ?> ⚡",
      "item": "<?= $site_url ?>/#heading-style-h1"
    }
  ]
}
</script>

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "<?= $site_name ?>",
  "operatingSystem": "ANDROID, iOS",
  "applicationCategory": "FinanceApplication",
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "<?= $rating_value ?>",
    "ratingCount": "<?= $rating_count ?>"
  },
  "offers": {
    "@type": "Offer",
    "price": "<?= $app_price ?>",
    "priceCurrency": "<?= $app_currency ?>"
  }
}
</script>
  <link rel="stylesheet" href="./integration/default-integration.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/intl-tel-input@23.0.12/build/css/intlTelInput.css">
  <link rel="icon" type="image/png" href="./favicon-96x96.png" sizes="96x96" />
  <link rel="icon" type="image/svg+xml" href="./favicon.svg" />
  <link rel="shortcut icon" href="./favicon.ico" />
  <link rel="apple-touch-icon" sizes="180x180" href="./apple-touch-icon.png" />
  <link rel="manifest" href="site.webmanifest" />
  <link rel="stylesheet" href="fonts.css">
  <link rel="stylesheet" href="tailwind.css">
  <link rel="stylesheet" href="styles.css?v=1">
  <link href="app.css" rel="stylesheet">
 
  <meta name="description" content="<?= $contacts_description ?>">
  <title><?= $contacts_title ?></title>

    <style>
        .header-form {
            padding-bottom: 0 !important;
            margin-bottom: 40px;
        }

        .other-content img {
            margin: 15px auto !important;
        } 

        input:not([type="checkbox"]) {
          color: black;
        }
    </style>
</head>

<body class="overflow-x-hidden">
  <header class="header-mobile flex flex-col">
    <nav class="nav py-1 lg:py-5 border-b border-b-white/10">
      <div class="relative max-w-8xl px-4 mx-auto pt-8 lg:pt-0 flex items-center justify-center lg:justify-between">
        <a class="logo flex items-center gap-3" href="index.php">
          <img src="favicon-96x96.png" style="height: 41px" alt="logo">
          <div class="uppercase text-white">
            <h1><?= $source ?></h1>
          </div>
        </a>
<div
  class="absolute -top-1 left-0 w-full lg:w-auto lg:static px-5 py-1 lg:py-2 bg-primary-main lg:rounded-md text-white font-bold text-sm lg:text-base text-center">
  <?= $availability_badge_text ?>
  <strong class="text-base lg:text-lg font-black" data-slot-count="">
    <?= $availability_badge_count ?>
  </strong>
</div>

<script>
  document.addEventListener("DOMContentLoaded", function() {
    const counterElement = document.querySelector('strong[data-slot-count]');
    let count = 32; 

    setInterval(function() {
      if (count > 1) {
        count--;
        counterElement.textContent = count;
      }
    }, 15000);
  });
</script>
      </div>
    </nav>
    <div class="other-content">
<h1><?= $contact_heading ?></h1>

<p><?= $contact_intro ?></p>

<h3><?= $contact_subheading ?></h3>

<p><?= $contact_text ?></p>

<ul>
  <li><?= $contact_list_1 ?></li>
  <li><?= $contact_list_2 ?></li>
  <li><?= $contact_list_3 ?></li>
  <li><?= $contact_list_4 ?></li>
  <li><?= $contact_list_5 ?></li>
  <li><?= $contact_list_6 ?></li>
</ul>

            <div class="header-lines flex flex-col flex-grow">
        <div class="flex flex-col lg:flex-row flex-grow">
          
          <div
            class="header-form pt-12 mx-auto w-full max-w-[420px] lg:max-w-[490px] flex flex-col items-center"
            id="testtest">
            <img class="w-12" src="favicon-96x96.png" alt="logo" style="width: 48px; height: 48px;">
<div class="mt-1 text-2xl font-black text-white font-alt form-title">
  <?= $form_heading ?>
</div>

<style>
  input {
    border-radius: 10px !important;
    padding-top: 25px !important;
    padding-bottom: 25px !important;
  }

    .input-phone {
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    width: 100% !important;
  }

    @media (max-width: 444px) {
  .iti.iti--allow-dropdown {
    width: auto !important;
  }
}
</style>

<form
  action="./integration/send.php" method="post"
  id="form-89301" class="leadform rf-form js-rf-form">

  <input type="hidden" name="js_token" value="<?= $jsToken; ?>">

  <div style="position:absolute; left:-9999px; opacity:0; height:0; overflow:hidden;">
    <input type="text" name="website" tabindex="-1" autocomplete="off">
    <input type="text" name="company" style="position:absolute; left:-9999px;">
  </div>

  <input type="hidden" name="country" value="<?= $form_country; ?>">
  <input type="hidden" name="language" value="<?= $form_language; ?>">
  <input type="hidden" name="phone_country" value="<?= $form_phone_country; ?>">
  <input type="hidden" name="only_countries" value='<?= $form_only_countries; ?>'>

  <div class="form-preloader hidden">
    <svg width="50" height="50" class="spinner" viewBox="0 0 50 50">
      <circle class="path" cx="25" cy="25" r="20" fill="none" stroke-width="5"></circle>
    </svg>
  </div>

  <div class="step">
    <div class="input-wrap">
      <input type="text" name="fname" id="f_name-89301"
        placeholder="<?= $form_placeholder_fname ?>" required>

      <div class="input-wrap">
        <input type="text" name="lname" id="l_name-89301"
          placeholder="<?= $form_placeholder_lname ?>" required>

        <div class="input-wrap">
          <input type="email" name="email" id="email-89301"
            placeholder="<?= $form_placeholder_email ?>" required>
        </div>
      </div>

      <div class="step">
<div class="input-phone" style="margin: 0 auto;">
        <input type="tel" autocomplete="off" id="phone-89301"  name="fullphone"
          placeholder="" required tabindex="0" class="vti__input">
</div>

        <span class="error-msg hide"></span>
      </div>
    </div>

    <div class="input-wrap">
      <button type="submit" class="submit">
        <?= $form_button_submit ?>
      </button>
    </div>
  </div>
</form>
            <div class="h-26 flex payment-methods">
              <img src="payment.svg" alt="">
            </div>
          </div>
        </div>
      </div>
      <p><?= $contact_form_text ?></p>
    </div>
  </header>
  <main class="main">
    <style>
      .images-max-width img {
        max-width: 400px !important;
        height: auto;
      }
    </style>
    </div>
  </main>
<footer class="footer pt-5 lg:pt-7 bg-primary-dark text-white">

  <div class="w-full max-w-8xl mx-auto px-3 md:px-6">
    <div class="flex flex-col lg:flex-row items-center justify-between">

      <div class="flex flex-col lg:flex-row items-center">
        <a class="logo flex items-center gap-3" href="index.php">
          <img src="favicon-96x96.png" style="height: 41px" alt="logo">

          <div class="uppercase text-white">
            <productname><?= $source ?></productname>
          </div>
        </a>

        <span class="lg:pl-5 lg:ml-5 lg:border-l lg:border-l-white/10">
          <?= $footer_tagline ?>
        </span>
      </div>

      <div class="w-full md:w-auto mt-4 md:mt-0 mx-4 md:order-2 flex flex-wrap items-center justify-center gap-y-1 gap-5 lg:gap-10">

        <a class="text-white hover:text-primary" href="about-us.php">
          <?= $footer_menu_about ?>
        </a>

        <a class="text-white hover:text-primary" href="contacts.php">
          <?= $footer_menu_contacts ?>
        </a>

        <a class="text-white hover:text-primary" href="sign-up.php">
          <?= $footer_menu_signup ?>
        </a>

        <a class="text-white hover:text-primary" href="private-policy.php">
          <?= $footer_menu_privacy ?>
        </a>

        <a class="text-white hover:text-primary" href="conditions.php">
          <?= $footer_menu_terms ?>
        </a>

      </div>
    </div>
  </div>

  <div class="w-full max-w-8xl mx-auto px-3 md:px-6 text-center md:text-left text-white/30 text-xs">
    <div class="my-5">
      <?= $footer_disclaimer_text ?>
    </div>
  </div>

  <div class="border-t border-t-white/10">
    <div class="w-full max-w-8xl mx-auto px-3 md:px-6">
      <div class="pt-5 flex flex-col md:flex-row items-center justify-center text-center text-sm">

        <div class="mb-5" style="padding-bottom: 50px">
          <?= $footer_copyright_text ?>

          <a class="text-white hover:text-primary" href="index.php">
            <productname><?= $source ?></productname>
          </a>
        </div>

      </div>
    </div>
  </div>

</footer>


  
  <script src="https://cdn.jsdelivr.net/npm/intl-tel-input@23.0.12/build/js/intlTelInput.min.js"></script>
  <script src="./integration/validation.js"></script>

</body>
</html>
