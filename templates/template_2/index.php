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
      "name": "⭐️ <?= $site_name ?> ⭐️",
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
<style>
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
<style>
  @media (max-width: 1024px) {
    .info-ph {
      max-width: 400px;
      max-height: 400px;
    }
  }
</style>
  <link rel="stylesheet" href="./integration/default-integration.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/intl-tel-input@23.0.12/build/css/intlTelInput.css">

  <meta name="description" content="<?= $main_description ?>">
  <title><?= $main_title ?></title>
  <link rel="icon" type="image/png" href="./favicon-96x96.png" sizes="96x96" />
  <link rel="icon" type="image/svg+xml" href="./favicon.svg" />
  <link rel="shortcut icon" href="./favicon.ico" />
  <link rel="apple-touch-icon" sizes="180x180" href="./apple-touch-icon.png" />
  <link rel="manifest" href="site.webmanifest" />
  <link rel="stylesheet" href="fonts.css">
  <link rel="stylesheet" href="tailwind.css">
  <link rel="stylesheet" href="styles.css?v=1">
  <link href="app.css" rel="stylesheet">
 
   
</head>

<body class="overflow-x-hidden">
  <header id="form-89301" class="header-mobile flex flex-col">
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
    <div class="relative w-full max-w-8xl px-4 mx-auto z-10 flex-grow flex flex-col">
      <div class="header-lines flex flex-col flex-grow">
        <div class="flex flex-col lg:flex-row flex-grow">
          <div class="w-full lg:w-1/2 my-6 text-center lg:text-left lg:self-center">
  <div class="text-3xl xl:text-5xl xl:leading-tight font-alt font-black text-white">
    <?= $hero_main_heading ?>
  </div>

  <div class="text-4xl xl:text-6xl xl:leading-tight font-alt font-black text-primary-bright">
    <?= $hero_main_highlight ?>
  </div>

  <div class="flex items-center justify-center lg:justify-start">
    <div class="my-2 text-base xl:text-2xl font-alt font-black text-white text-left">
      <?= $hero_main_subtext ?>
    </div>

    <div class="ml-4 p-1.5 rounded-full bg-primary-darker flex gap-1 items-center">
      <img class="w-7 h-7 lg:w-9 lg:h-9" src="btc.svg" alt="">
      <img class="w-7 h-7 lg:w-9 lg:h-9" src="usdt.svg" alt="">
      <img class="w-7 h-7 lg:w-9 lg:h-9" src="binance.svg" alt="">
      <img class="mx-2" src="header-arrow.svg" alt="">
    </div>
  </div>

  <div class="my-5 lg:my-10 text-base md:text-lg font-semibold text-white/80">
    <?= $hero_main_description ?>
  </div>

  <div class="flex items-center justify-center lg:justify-start gap-2 xl:gap-5">
    <div class="flex">
      <img class="relative w-11 h-11 rounded-full border border-primary-dark z-[3]" src="header-avatar-1.webp"
        srcset="header-avatar-1.webp 1x, header-avatar-1@2x.webp 2x" alt="">
      <img class="relative w-11 h-11 -ml-3 rounded-full border border-primary-dark z-[2]"
        src="header-avatar-2.webp" srcset="header-avatar-2.webp 1x, header-avatar-2@2x.webp 2x" alt="">
      <img class="relative w-11 h-11 -ml-3 rounded-full border border-primary-dark z-[1]"
        src="header-avatar-3.webp" srcset="header-avatar-3.webp 1x, header-avatar-3@2x.webp 2x" alt="">
    </div>

    <div class="text-left text-xs sm:text-base">
      <div class="text-white">
        <span class="text-white/80"><?= $hero_rating_text_prefix ?></span>
        <span class="font-bold"><?= $hero_rating_users ?></span>
      </div>
      <img class="h-5" src="stars.svg" alt="">
    </div>
  </div>
</div>
          <div
            class="header-form pt-12 mx-auto lg:ml-auto lg:mr-0 w-full max-w-[420px] lg:max-w-[490px] flex flex-col items-center"
            style="margin: 0 auto !important;"
            id="testtest">
            <img class="w-12" src="favicon-96x96.png" alt="logo">
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
    </div>
  </header>
  <main class="main">
    <style>
      .images-max-width img {
        max-width: 400px !important;
        height: auto;
      }
    </style>
   <div class="my-7 lg:my-12 w-full max-w-8xl px-4 mx-auto images-max-width">
  <div class="mb-4 md:mb-16 flex flex-col md:flex-row border border-primary-dark/10 rounded-xl">
    <div class="md:order-2 md:w-1/3 lg:w-auto md:-mr-px flex-shrink-0">
      <img class="w-full block rounded-t-xl md:rounded-br-xl" src="person-1.jpg" alt="person">
    </div>
    <div class="flex-grow p-4 sm:p-7">
      <div class="flex items-center">
        <img class="w-12 sm:w-auto mr-4 sm:mr-6" src="quote.svg" alt="">
        <div>
          <div class="text-primary-darker text-xl lg:text-2xl font-black font-alt">
            <person1><?= $expert1_name ?></person1>
          </div>
          <div class="text-sm uppercase font-bold text-primary-medium">
            <?= $expert1_position ?>
          </div>
        </div>
      </div>
      <div class="mt-4 sm:mt-7 text-primary-medium lg:text-lg">
        <?= $expert1_text ?>
      </div>
    </div>
  </div>

  <div class="flex flex-col md:flex-row border border-primary-dark/10 rounded-xl md:rounded-bl-none">
    <div class="md:w-1/3 lg:w-auto md:-ml-px flex-shrink-0">
      <img class="w-full block rounded-t-xl md:rounded-br-xl" src="person-2.jpg" alt="person">
    </div>
    <div class="flex-grow p-4 sm:p-7">
      <div class="flex items-center">
        <img class="w-12 sm:w-auto mr-4 sm:mr-6" src="quote.svg" alt="">
        <div>
          <div class="text-primary-darker text-xl lg:text-2xl font-black font-alt">
            <person2><?= $expert2_name ?></person2>
          </div>
          <div class="text-sm uppercase font-bold text-primary-medium">
            <?= $expert2_position ?>
          </div>
        </div>
      </div>
      <div class="mt-4 sm:mt-7 text-primary-medium lg:text-lg">
        <?= $expert2_text ?>
      </div>
    </div>
  </div>
</div>
    <div class="my-7 lg:my-12 w-full max-w-8xl px-4 mx-auto">
  <div class="mb-7 grid grid-cols-1 lg:grid-cols-3 gap-4 lg:gap-7 lg:items-center">

    <div class="lg:col-span-2">
      <div class="mb-2 text-sm uppercase font-black text-primary-medium">
        <h2><?= $section01_title_number ?></h2>
      </div>

      <div class="text-primary-darker text-xl lg:text-2xl font-black font-alt">
        <?= $section01_heading ?>
      </div>
    </div>

    <a href="index.php#form-89301">
      <div class="lg:flex lg:justify-end text-primary-medium">
        <button class="h-12 px-4 sm:px-6 border-0 rounded-md text-white font-black font-alt cursor-pointer bg-primary-bright active:brightness-95 hover:brightness-105 text-sm sm:text-base whitespace-nowrap">
          <?= $section01_button_text ?>
        </button>
      </div>
    </a>

  </div>

  <div class="phones-bg rounded-xl">
    <div class="relative phones-lines pb-64 lg:pb-0 mb-24">

      <div class="py-7 px-2.5 sm:py-10 lg:p-14 xl:px-20 xl:py-24 flex flex-col md:flex-row md:justify-between md:gap-2.5">

        <!-- LEFT COLUMN -->
        <div class="mb-2.5 md:mb-0 min-w-[300px] flex flex-col md:flex-grow lg:flex-grow-0 gap-2.5">

          <!-- BTC -->
          <div class="w-full flex items-center px-5 py-2.5 rounded-lg bg-white/5">
            <img class="w-9 h-9 mr-4" src="btc.svg" alt="">
            <div class="mr-auto">
              <div class="mb-1 text-lg font-alt font-black text-white uppercase leading-4">BTC</div>
              <div class="text-white/40 leading-4"><?= $coin_btc_name ?></div>
            </div>
            <div class="text-[#75C22B] text-lg font-black">
              <?= $coin_btc_profit ?>
            </div>
          </div>

          <!-- ETH -->
          <div class="w-full flex items-center px-5 py-2.5 rounded-lg bg-white/5">
            <img class="w-9 h-9 mr-4" src="eth.svg" alt="">
            <div class="mr-auto">
              <div class="mb-1 text-lg font-alt font-black text-white uppercase leading-4">ETH</div>
              <div class="text-white/40 leading-4"><?= $coin_eth_name ?></div>
            </div>
            <div class="text-[#75C22B] text-lg font-black">
              <?= $coin_eth_profit ?>
            </div>
          </div>

          <!-- LTC -->
          <div class="w-full flex items-center px-5 py-2.5 rounded-lg bg-white/5">
            <img class="w-9 h-9 mr-4" src="ltc.svg" alt="">
            <div class="mr-auto">
              <div class="mb-1 text-lg font-alt font-black text-white uppercase leading-4">LTC</div>
              <div class="text-white/40 leading-4"><?= $coin_ltc_name ?></div>
            </div>
            <div class="text-[#75C22B] text-lg font-black">
              <?= $coin_ltc_profit ?>
            </div>
          </div>

        </div>

        <!-- RIGHT COLUMN -->
        <div class="min-w-[300px] flex flex-col md:flex-grow lg:flex-grow-0 gap-2.5">

          <!-- BTC -->
          <div class="w-full flex items-center px-5 py-2.5 rounded-lg bg-white/5">
            <img class="w-9 h-9 mr-4" src="btc.svg" alt="">
            <div class="mr-auto">
              <div class="mb-1 text-lg font-alt font-black text-white uppercase leading-4">BTC</div>
              <div class="text-white/40 leading-4"><?= $coin_btc_name ?></div>
            </div>
            <div class="text-[#75C22B] text-lg font-black">
              <?= $coin_btc_profit ?>
            </div>
          </div>

          <!-- ETH -->
          <div class="w-full flex items-center px-5 py-2.5 rounded-lg bg-white/5">
            <img class="w-9 h-9 mr-4" src="eth.svg" alt="">
            <div class="mr-auto">
              <div class="mb-1 text-lg font-alt font-black text-white uppercase leading-4">ETH</div>
              <div class="text-white/40 leading-4"><?= $coin_eth_name ?></div>
            </div>
            <div class="text-[#75C22B] text-lg font-black">
              <?= $coin_eth_profit ?>
            </div>
          </div>

          <!-- LTC -->
          <div class="w-full flex items-center px-5 py-2.5 rounded-lg bg-white/5">
            <img class="w-9 h-9 mr-4" src="ltc.svg" alt="">
            <div class="mr-auto">
              <div class="mb-1 text-lg font-alt font-black text-white uppercase leading-4">LTC</div>
              <div class="text-white/40 leading-4"><?= $coin_ltc_name ?></div>
            </div>
            <div class="text-[#75C22B] text-lg font-black">
              <?= $coin_ltc_profit ?>
            </div>
          </div>

        </div>

      </div>

      <img class="absolute left-1/2 bottom-0 lg:bottom-1/2 -translate-x-1/2 translate-y-[20%] lg:translate-y-1/2 w-72"
        src="phones.webp"
        srcset="phones.webp 1x, phones@2x.webp 2x"
        alt="">
    </div>
  </div>
</div>
<div class="my-7 lg:my-12 w-full max-w-8xl px-4 mx-auto">

  <div class="mb-7 grid grid-cols-1 lg:grid-cols-3 gap-4 lg:gap-7 lg:items-center">
    <div class="lg:col-span-2">
      <div class="mb-2 text-sm uppercase font-black text-primary-medium">
        <h2><?= $section02_title_number ?></h2>
      </div>

      <div class="text-primary-darker text-xl lg:text-2xl font-black font-alt">
        <?= $section02_heading ?>
      </div>
    </div>

    <div class="lg:text-lg text-primary-medium">
      <?= $section02_right_text ?>
    </div>
  </div>

  <div class="grid grid-cols-1 gap-4 lg:grid-cols-3 lg:gap-7">

    <!-- TESTIMONIAL 1 -->
    <div class="p-4 sm:p-7 rounded-lg bg-primary-light flex flex-col items-start">
      <img class="h-5" src="stars.svg" alt="">
      <div class="my-5 pb-5 flex-grow text-primary-medium border-b border-b-primary-dark/10">
        <?= $test1_text ?>
      </div>

      <div class="flex items-center">
        <div class="w-16 h-16 sm:w-20 sm:h-20 mr-5 flex-shrink-0 rounded-full">
          <img class="block w-full h-full object-cover rounded-full" src="user-1.webp"
            srcset="user-1.webp 1x, user-1@2x.webp 2x" alt="">
        </div>

        <div>
          <div class="font-black font-alt text-primary-darker truncate sm:text-lg">
            <?= $test1_name ?>
          </div>

          <div class="px-4 py-1 inline-block rounded bg-primary-main text-white text-lg font-alt font-black">
            <?= $test1_profit ?>
          </div>
        </div>
      </div>
    </div>

    <!-- TESTIMONIAL 2 -->
    <div class="p-4 sm:p-7 rounded-lg bg-primary-light flex flex-col items-start">
      <img class="h-5" src="stars.svg" alt="">
      <div class="my-5 pb-5 flex-grow text-primary-medium border-b border-b-primary-dark/10">
        <?= $test2_text ?>
      </div>

      <div class="flex items-center">
        <div class="w-16 h-16 sm:w-20 sm:h-20 mr-5 flex-shrink-0 rounded-full">
          <img class="block w-full h-full object-cover rounded-full" src="user-2.webp"
            srcset="user-2.webp 1x, user-2@2x.webp 2x" alt="">
        </div>

        <div>
          <div class="font-black font-alt text-primary-darker truncate sm:text-lg">
            <?= $test2_name ?>
          </div>

          <div class="px-4 py-1 inline-block rounded bg-primary-main text-white text-lg font-alt font-black">
            <?= $test2_profit ?>
          </div>
        </div>
      </div>
    </div>

    <!-- TESTIMONIAL 3 -->
    <div class="p-4 sm:p-7 rounded-lg bg-primary-light flex flex-col items-start">
      <img class="h-5" src="stars.svg" alt="">
      <div class="my-5 pb-5 flex-grow text-primary-medium border-b border-b-primary-dark/10">
        <?= $test3_text ?>
      </div>

      <div class="flex items-center">
        <div class="w-16 h-16 sm:w-20 sm:h-20 mr-5 flex-shrink-0 rounded-full">
          <img class="block w-full h-full object-cover rounded-full" src="user-3.webp"
            srcset="user-3.webp 1x, user-3@2x.webp 2x" alt="">
        </div>

        <div>
          <div class="font-black font-alt text-primary-darker truncate sm:text-lg">
            <?= $test3_name ?>
          </div>

          <div class="px-4 py-1 inline-block rounded bg-primary-main text-white text-lg font-alt font-black">
            <?= $test3_profit ?>
          </div>
        </div>
      </div>
    </div>

  </div>
</div>
<div class="pros-bg">
  <div class="py-7 lg:py-12 w-full max-w-8xl px-4 mx-auto">

    <div class="mb-2 text-sm uppercase font-black text-[#7389a3]">
      <h2><?= $pros_section_number ?></h2>
    </div>

    <div class="mb-7 grid grid-cols-1 lg:grid-cols-3 gap-4 lg:gap-7 lg:items-center">

      <div class="lg:col-span-2">
        <div class="text-white text-xl lg:text-2xl font-black font-alt">
          <?= $pros_main_heading ?>
        </div>
      </div>

      <div class="lg:text-lg text-[#7389a3]">
        <?= $pros_subtext ?>
      </div>

    </div>

    <div class="grid grid-cols-1 gap-4 lg:grid-cols-3 lg:gap-7">

      <!-- CARD 1 -->
      <div class="border-l border-l-white/10 border-b border-b-white/10 p-4 sm:p-7 !pr-0">
        <div class="mb-4 sm:mb-7 sm:max-w-60 text-white sm:text-lg font-black font-alt">
          <?= $pros1_title ?>
        </div>

        <div class="flex items-start">
          <img class="w-16 h-16 sm:w-20 sm:h-20 mr-4 sm:mr-7" src="pros-1.svg" alt="">
          <div class="text-white">
            <?= $pros1_text ?>
          </div>
        </div>
      </div>

      <!-- CARD 2 -->
      <div class="border-l border-l-white/10 border-b border-b-white/10 p-4 sm:p-7 !pr-0">
        <div class="mb-4 sm:mb-7 sm:max-w-60 text-white sm:text-lg font-black font-alt">
          <?= $pros2_title ?>
        </div>

        <div class="flex items-start">
          <img class="w-16 h-16 sm:w-20 sm:h-20 mr-4 sm:mr-7" src="pros-2.svg" alt="">
          <div class="text-white">
            <?= $pros2_text ?>
          </div>
        </div>
      </div>

      <!-- CARD 3 -->
      <div class="border-l border-l-white/10 border-b border-b-white/10 p-4 sm:p-7 !pr-0">
        <div class="mb-4 sm:mb-7 sm:max-w-60 text-white sm:text-lg font-black font-alt">
          <?= $pros3_title ?>
        </div>

        <div class="flex items-start">
          <img class="w-16 h-16 sm:w-20 sm:h-20 mr-4 sm:mr-7" src="pros-3.svg" alt="">
          <div class="text-white">
            <?= $pros3_text ?>
          </div>
        </div>
      </div>

    </div>

  </div>
</div>

<div class="my-7 lg:my-12 w-full max-w-8xl px-4 mx-auto">
  <div class="grid grid-cols-1 gap-4 lg:grid-cols-3 lg:gap-7">

    <div class="relative">
      <img class="w-full h-full rounded-xl info-ph" src="info.webp"
        srcset="info.webp 1x, info@2x.webp 2x" alt="">
    </div>

    <div class="lg:col-span-2">

      <div class="mb-2 text-sm uppercase font-black text-primary-medium">
        <h2><?= $about_section_number ?></h2>
      </div>

      <div class="text-primary-darker text-xl lg:text-2xl font-black font-alt">
        <?= $about_heading ?>
      </div>

      <div class="my-4 lg:my-7 text-primary-medium lg:text-lg">
        <?= $about_text ?>
      </div>

      <div class="flex flex-col sm:flex-row items-center lg:-translate-x-1/3">

        <div class="p-4 sm:px-8 sm:py-6 rounded-xl bg-primary-light/90 flex items-center gap-2 sm:gap-2.5">
          <div class="max-w-12"><img class="block" src="coinbase.svg" alt=""></div>
          <div class="max-w-12"><img class="block" src="kraken.svg" alt=""></div>
          <div class="max-w-12"><img class="block" src="binance.svg" alt=""></div>
          <div class="max-w-12"><img class="block" src="polonex.svg" alt=""></div>
          <div class="max-w-12"><img class="block" src="bittrex.svg" alt=""></div>
          <div class="sm:ml-4">
            <img class="max-w-12 sm:max-w-none block rotate-90 sm:rotate-0" src="info-arrow.svg" alt="">
          </div>
        </div>

        <a href="index.php#">
          <button class="h-12 mt-4 sm:mt-0 px-4 sm:px-6 sm:ml-7 border-0 rounded-md text-white font-black font-alt cursor-pointer bg-primary-bright active:brightness-95 hover:brightness-105 text-sm sm:text-base whitespace-nowrap">
            <?= $about_button_text ?>
          </button>
        </a>

      </div>

    </div>
  </div>
</div>
    <div class="bg-primary-dark">
      <div class="py-7 lg:py-12 w-full max-w-8xl px-4 mx-auto">
  <div class="grid grid-cols-1 gap-4 lg:grid-cols-3 lg:gap-7">

    <!-- TEST 4 -->
    <div class="p-4 sm:p-7 rounded-lg bg-primary-light flex flex-col items-start">
      <img class="h-5" src="stars.svg" alt="">

      <div class="my-5 pb-5 flex-grow text-primary-medium border-b border-b-primary-dark/10">
        <?= $test4_text ?>
      </div>

      <div class="flex items-center">
        <div class="w-16 h-16 sm:w-20 sm:h-20 mr-5 flex-shrink-0 rounded-full">
          <img class="block w-full h-full object-cover rounded-full" src="user-4.webp"
            srcset="user-4.webp 1x, user-4@2x.webp 2x" alt="">
        </div>

        <div>
          <div class="font-black font-alt text-primary-darker truncate sm:text-lg">
            <?= $test4_name ?>
          </div>

          <div class="px-4 py-1 inline-block rounded bg-primary-main text-white text-lg font-alt font-black">
            <?= $test4_profit ?>
          </div>
        </div>
      </div>
    </div>

    <!-- TEST 5 -->
    <div class="p-4 sm:p-7 rounded-lg bg-primary-light flex flex-col items-start">
      <img class="h-5" src="stars.svg" alt="">

      <div class="my-5 pb-5 flex-grow text-primary-medium border-b border-b-primary-dark/10">
        <?= $test5_text ?>
      </div>

      <div class="flex items-center">
        <div class="w-16 h-16 sm:w-20 sm:h-20 mr-5 flex-shrink-0 rounded-full">
          <img class="block w-full h-full object-cover rounded-full" src="user-5.webp"
            srcset="user-5.webp 1x, user-5@2x.webp 2x" alt="">
        </div>

        <div>
          <div class="font-black font-alt text-primary-darker truncate sm:text-lg">
            <?= $test5_name ?>
          </div>

          <div class="px-4 py-1 inline-block rounded bg-primary-main text-white text-lg font-alt font-black">
            <?= $test5_profit ?>
          </div>
        </div>
      </div>
    </div>

    <!-- TEST 6 -->
    <div class="p-4 sm:p-7 rounded-lg bg-primary-light flex flex-col items-start">
      <img class="h-5" src="stars.svg" alt="">

      <div class="my-5 pb-5 flex-grow text-primary-medium border-b border-b-primary-dark/10">
        <?= $test6_text ?>
      </div>

      <div class="flex items-center">
        <div class="w-16 h-16 sm:w-20 sm:h-20 mr-5 flex-shrink-0 rounded-full">
          <img class="block w-full h-full object-cover rounded-full" src="user-6.webp"
            srcset="user-6.webp 1x, user-6@2x.webp 2x" alt="">
        </div>

        <div>
          <div class="font-black font-alt text-primary-darker truncate sm:text-lg">
            <?= $test6_name ?>
          </div>

          <div class="px-4 py-1 inline-block rounded bg-primary-main text-white text-lg font-alt font-black">
            <?= $test6_profit ?>
          </div>
        </div>
      </div>
    </div>

  </div>
</div>



    </div>
    <div class="bg-primary-light">
  <div class="py-7 w-full max-w-8xl px-4 mx-auto">

    <!-- TEST 1 -->
    <div class="flex flex-col lg:flex-row lg:items-center">
      <div class="lg:w-1/3 mb-4 lg:mb-0 flex items-center flex-shrink-0">

        <div class="w-16 h-16 sm:w-20 sm:h-20 mr-5 flex-shrink-0 rounded-full">
          <img class="block w-full h-full object-cover rounded-full"
            src="user-7.webp"
            srcset="user-7.webp 1x, user-7@2x.webp 2x" alt="">
        </div>

        <div>
          <div class="font-black font-alt text-primary-darker truncate sm:text-lg">
            <?= $single_test1_name ?>
          </div>

          <img class="h-5" src="stars.svg" alt="">

          <div class="mt-2 flex gap-2">
            <a class="like-trigger px-2 py-0.5 inline-flex items-center border border-primary-medium rounded text-primary-medium hover:text-primary-main hover:border-primary-main active:brightness-95"
              href="javascript:void(0)">
              <i class="icon-like mr-1"></i><?= $single_test1_i ?>
            </a>
          </div>
        </div>
      </div>

      <div class="flex-grow text-primary-medium">
        <?= $single_test1_text ?>
      </div>
    </div>

  </div>
</div>

<div class="bg-white">
  <div class="py-7 w-full max-w-8xl px-4 mx-auto">

    <!-- TEST 2 -->
    <div class="flex flex-col lg:flex-row lg:items-center">
      <div class="lg:w-1/3 mb-4 lg:mb-0 flex items-center flex-shrink-0">

        <div class="w-16 h-16 sm:w-20 sm:h-20 mr-5 flex-shrink-0 rounded-full">
          <img class="block w-full h-full object-cover rounded-full"
            src="user-8.webp"
            srcset="user-8.webp 1x, user-8@2x.webp 2x" alt="">
        </div>

        <div>
          <div class="font-black font-alt text-primary-darker truncate sm:text-lg">
            <?= $single_test2_name ?>
          </div>

          <img class="h-5" src="stars.svg" alt="">

          <div class="mt-2 flex gap-2">
            <a class="like-trigger px-2 py-0.5 inline-flex items-center border border-primary-medium rounded text-primary-medium hover:text-primary-main hover:border-primary-main active:brightness-95"
              href="javascript:void(0)">
              <i class="icon-like mr-1"></i><?= $single_test1_i ?>
            </a>
          </div>
        </div>
      </div>

      <div class="flex-grow text-primary-medium">
        <?= $single_test2_text ?>
      </div>
    </div>

  </div>
</div>

<div class="bg-primary-light">
  <div class="py-7 w-full max-w-8xl px-4 mx-auto">

    <!-- TEST 3 -->
    <div class="flex flex-col lg:flex-row lg:items-center">
      <div class="lg:w-1/3 mb-4 lg:mb-0 flex items-center flex-shrink-0">

        <div class="w-16 h-16 sm:w-20 sm:h-20 mr-5 flex-shrink-0 rounded-full">
          <img class="block w-full h-full object-cover rounded-full"
            src="user-9.webp"
            srcset="user-9.webp 1x, user-9@2x.webp 2x" alt="">
        </div>

        <div>
          <div class="font-black font-alt text-primary-darker truncate sm:text-lg">
            <?= $single_test3_name ?>
          </div>

          <img class="h-5" src="stars.svg" alt="">

          <div class="mt-2 flex gap-2">
            <a class="like-trigger px-2 py-0.5 inline-flex items-center border border-primary-medium rounded text-primary-medium hover:text-primary-main hover:border-primary-main active:brightness-95"
              href="javascript:void(0)">
              <i class="icon-like mr-1"></i><?= $single_test1_i ?>
            </a>
          </div>
        </div>
      </div>

      <div class="flex-grow text-primary-medium">
        <?= $single_test3_text ?>
      </div>
    </div>

  </div>
</div>
    
    <a class="logo flex items-center gap-3" href="index.php#">


      <div class="my-7 lg:my-12 w-full max-w-8xl px-4 mx-auto">
<div class="p-7 rounded-xl bg-primary-main text-white text-xl lg:text-2xl font-black font-alt text-center">
  <?= $live_counter_text_prefix ?>
  <strong data-slot-count2=""><?= $live_counter_value ?></strong>
  <?= $live_counter_text_suffix ?>
</div>
      </div>
    </a>
    <div class="bg-primary-light">
      <div class="w-full max-w-8xl lg:px-4 mx-auto flex flex-col lg:flex-row lg:items-center">

  <div class="relative w-full pt-[56.25%] lg:pt-0 lg:w-96 lg:min-h-[454px] flex-shrink-0">
    <img class="absolute top-0 right-0 w-full h-full object-cover lg:w-auto lg:max-w-none"
      src="bottom.webp"
      srcset="bottom.webp 1x, bottom@2x.webp 2x"
      alt="">
  </div>

  <div class="px-4 lg:px-12 py-4 text-center lg:text-left">

    <div class="text-2xl md:text-4xl font-black text-primary-darker font-alt">
      <?= $bottom_cta_heading ?>
    </div>

    <div class="mt-4 text-2xl md:text-4xl font-light font-alt text-primary-medium">
      <?= $bottom_cta_subheading ?>
    </div>

  </div>

</div>
          <div class="relative w-full px-4 mx-auto z-10 flex-grow flex flex-col" style="background-image: url(header-bg2@2x.webp); background-position: center;">
      <div class="header-lines flex flex-col flex-grow">
        <div class="flex flex-col lg:flex-row flex-grow">
          
          <div
            class="header-form pt-12 mx-auto w-full max-w-[420px] lg:max-w-[490px] flex flex-col items-center"
            id="testtest">
            <img class="w-12" src="favicon-96x96.png" alt="logo">
<div class="mt-1 text-2xl font-black text-white font-alt form-title">
  <?= $form_heading ?>
</div>

<style>
  input {
    border-radius: 10px !important;
    padding-top: 25px !important;
    padding-bottom: 25px !important;
  }
</style>

<form
  action="./integration/send.php" method="post" class="leadform rf-form js-rf-form">

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





    </div>
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


  
<script>
document.querySelectorAll(".like-trigger").forEach(button => {
  button.addEventListener("click", function(e) {
    e.preventDefault();
    
    const icon = this.querySelector("i");
    if (icon) {
      icon.classList.toggle("active");
    }
  
    this.classList.toggle("active");
  });
});
</script>

<script>
document.addEventListener("click", function(e){

  const link = e.target.closest("a");
  if (!link) return;

  const href = link.getAttribute("href");

  if (!href || !href.startsWith("#")) return;

  const target = document.querySelector(href);
  if (!target) return;

  e.preventDefault();

  target.scrollIntoView({
    behavior: "smooth",
    block: "start"
  });

});
</script>

  <script src="https://cdn.jsdelivr.net/npm/intl-tel-input@23.0.12/build/js/intlTelInput.min.js"></script>
  <script src="./integration/validation.js"></script>

</body>
</html>
