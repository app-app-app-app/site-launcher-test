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
<html lang="<?= $site_lang ?>" style="filter: hue-rotate(3deg);">

<head>
<?php
$host = $_SERVER['HTTP_HOST'];
$uri = strtok($_SERVER['REQUEST_URI'], '?'); // без GET-параметрів

$canonical = 'https://' . $host . $uri;
?>

<link rel="canonical" href="<?= htmlspecialchars($canonical, ENT_QUOTES, 'UTF-8'); ?>" />
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
      "name": "💰 <?= $site_name ?> 💰",
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
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, minimum-scale=1, maximum-scale=1">
  <link rel="shortcut icon" href="./favicon.svg" type="image/x-icon">
  <title><?= $page_title_main ?></title>
  <meta name="description" content="<?= $page_description_main ?>">
  <link rel="stylesheet" href="css/swiper-bundle.min.css">
  <link rel="stylesheet" href="css/main-1.css">
  <link rel="icon" type="image/png" href="./favicon-96x96.png" sizes="96x96" />
  <link rel="icon" type="image/svg+xml" href="./favicon.svg" />
  <link rel="shortcut icon" href="./favicon.ico" />
  <link rel="apple-touch-icon" sizes="180x180" href="./apple-touch-icon.png" />
  <link rel="manifest" href="/site.webmanifest" />
  <link href="./integration/default-integration.css" rel="stylesheet"/>
  <link href="https://cdn.jsdelivr.net/npm/intl-tel-input@23.0.12/build/css/intlTelInput.css" rel="stylesheet"/>

</head>

<body>

<header class="header" data-js-header="">
  <div class="header__body">
    <div class="header__body-inner container">
      <a class="header__logo logo" href="<?= $site_url ?>" aria-label="Home" title="Home">
        <svg xmlns="http://www.w3.org/2000/svg" width="40" height="30" viewBox="0 0 40 30" fill="none">
          <path d="M13.7943 11.3128L11.2695 13.8133C10.7876 14.2906 10.7876 15.0644 11.2695 15.5417L14.0506 18.296C14.5686 18.8089 15.8784 18.3232 16.3963 17.8103L18.5436 15.6837C18.7751 15.4545 18.9051 15.1436 18.9051 14.8195L18.9051 13.4828C18.9051 11.4578 20.5627 9.81625 22.6074 9.81625H26.2199C28.2646 9.81625 29.9222 11.4578 29.9222 13.4828L29.9222 17.0605C29.9222 19.0855 28.2646 20.7271 26.2199 20.7271H24.8704C24.5431 20.7271 24.2292 20.8558 23.9977 21.085L21.8503 23.2117C21.3324 23.7246 20.842 25.0218 21.3599 25.5347L24.141 28.289C24.623 28.7663 25.4044 28.7663 25.8863 28.289L28.5698 25.6314C28.888 25.3163 28.9929 24.8557 28.9446 24.4127C28.8142 23.2142 29.2128 21.9699 30.1404 21.0512C31.0681 20.1324 32.3245 19.7377 33.5347 19.8669C33.9821 19.9147 34.4472 19.8108 34.7653 19.4957L38.7578 15.5417C39.2398 15.0644 39.2398 14.2906 38.7578 13.8133L35.2063 10.2961C34.8734 9.96641 34.3816 9.87003 33.9148 9.93037C32.768 10.0786 31.5668 9.71648 30.6858 8.84399C29.8049 7.97151 29.4392 6.78192 29.5889 5.64622C29.6498 5.18394 29.5525 4.6968 29.2196 4.36715L25.8863 1.06598C25.4044 0.588683 24.623 0.588684 24.141 1.06598L20.3072 4.86278C19.9629 5.20374 19.8699 5.71135 19.9536 6.18634C20.1791 7.465 19.7932 8.8287 18.7961 9.81625C17.7989 10.8038 16.4219 11.1859 15.1308 10.9626C14.6512 10.8797 14.1386 10.9719 13.7943 11.3128Z" fill="#E3FF34"></path>
          <path d="M10.7081 4.21461L13.233 1.71415C13.7149 1.23685 14.4963 1.23685 14.9783 1.71415L17.7594 4.46844C18.2773 4.98137 17.7869 6.27854 17.2689 6.79146L15.1216 8.91808C14.8902 9.14728 14.5763 9.27605 14.249 9.27605H12.8993C10.8546 9.27605 9.19699 10.9176 9.19699 12.9426L9.19698 16.5203C9.19698 18.5453 10.8546 20.1869 12.8993 20.1869L16.5118 20.1869C18.5565 20.1869 20.2141 18.5453 20.2141 16.5203V15.1838C20.2141 14.8596 20.3441 14.5487 20.5756 14.3195L22.723 12.1929C23.2409 11.6799 24.5507 11.1942 25.0686 11.7072L27.8498 14.4614C28.3317 14.9387 28.3317 15.7126 27.8498 16.1899L25.1662 18.8475C24.8481 19.1626 24.383 19.2665 23.9356 19.2187C22.7255 19.0895 21.469 19.4843 20.5414 20.403C19.6137 21.3217 19.2151 22.566 19.3456 23.7645C19.3938 24.2075 19.2889 24.6681 18.9707 24.9832L14.9782 28.9372C14.4963 29.4145 13.7149 29.4145 13.233 28.9372L9.68147 25.42C9.3486 25.0903 9.25129 24.6032 9.31222 24.1409C9.4619 23.0052 9.09624 21.8156 8.21526 20.9431C7.33427 20.0706 6.1331 19.7085 4.98632 19.8567C4.51954 19.9171 4.02766 19.8207 3.69479 19.4911L0.361461 16.1899C-0.120487 15.7126 -0.120487 14.9387 0.361461 14.4614L4.19526 10.6646C4.53953 10.3237 5.05209 10.2315 5.53171 10.3145C6.82282 10.5378 8.19981 10.1556 9.19698 9.16808C10.1942 8.18053 10.58 6.81683 10.3546 5.53817C10.2708 5.06318 10.3639 4.55557 10.7081 4.21461Z" fill="#E3FF34"></path>
        </svg>
        <span><?= $source ?></span>
      </a>

      <div class="header__overlay" data-js-header-overlay="">
        <nav class="header__menu">
          <ul class="header__menu-list">
            <li class="header__menu-item">
              <a class="header__menu-link" href="<?= $site_url ?>#leaders"><?= $nav_investors ?></a>
            </li>
            <li class="header__menu-item">
              <a class="header__menu-link" href="<?= $site_url ?>#steps"><?= $nav_steps ?></a>
            </li>
            <li class="header__menu-item">
              <a class="header__menu-link" href="<?= $site_url ?>#trades"><?= $nav_trade ?></a>
            </li>
            <li class="header__menu-item">
              <a class="header__menu-link" href="<?= $site_url ?>#advantages"><?= $nav_advantages ?></a>
            </li>
            <li class="header__menu-item">
              <a class="header__menu-link" href="<?= $site_url ?>#statistics"><?= $nav_statistics ?></a>
            </li>
            <li class="header__menu-item">
              <a class="header__menu-link" href="<?= $site_url ?>#feedback"><?= $nav_feedback ?></a>
            </li>
          </ul>
        </nav>

        <a href="sign-up.php">
          <button class="header__button" type="button" data-js-button-form="">
            <?= $button_register ?>
          </button>
        </a>
      </div>

      <button class="header__burger-button burger-button visible-tablet" type="button" aria-label="Open menu" title="Open menu" data-js-header-burger-button="">
        <span class="burger-button__line"></span>
        <span class="burger-button__line"></span>
        <span class="burger-button__line"></span>
      </button>
    </div>
  </div>
  <span class="backdrop"></span>
</header>

  <main>
    <style>
      @media (max-width: 768px) {
        .welcome__main {
          padding-top: 0;
        }

        .welcome__title {
          margin-top: 1.5rem;
          z-index: 50;
          text-shadow: 2px 2px 5px #000000;
        }

        .welcome__form::before {

          filter: blur(2px);
          /* добавляем размытие */
        }

      }
    </style>
    <section class="welcome" aria-labelledby="welcome-title">
      <h1 class="hide-mobile" style="text-align:center; color:#e3ff34; padding:20px;"><?= $source ?></h1>
      <div class="welcome__main container">
        <div class="welcome__text">
          <span class="welcome__title" id="welcome-title">
            <?= $main_h1 ?>
          </span>
          <div class="welcome__badge">
            <img class="welcome__badge_img" src="<?= $crypto_img ?>" width="40" height="40" alt="flag">
            <p class="welcome__badge_text">
              <?= $main_p ?>
            </p>
          </div>
        </div>
        <div class="welcome__form">
          <div class="form">
            <style>
              .iti__country-container {
                pointer-events: none;
              }

              .iti__arrow {
                display: none;
              }

              .leadform {
                max-width: 400px;
                margin: 0 auto;
              }

              .leadform input {
                display: block;
                width: 100%;
                border-radius: 5px;
                border: 1px solid #ccc;
                margin: 20px 0;
                padding: 15px;
              }


              .form {
                padding: 20px !important;
              }
            </style>

            <form class="leadform rf-form js-rf-form" id="form" method="post" action="./integration/send.php">
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
                <circle class="path" cx="25" cy="25" r="20" fill="none"   stroke-width="5"></circle>
            </svg>
            </div>

            <input type="text" placeholder="<?= $contact_form_fname ?>" name="fname" required="">
            <input type="text" placeholder="<?= $contact_form_lname ?>" name="lname" required="">
            <input type="email" placeholder="<?= $contact_form_email ?>" name="email" required="">
            <input type="tel" name="fullphone" required="">
            <span class="error-msg hide"></span>
            <button type="submit" class="submit" style="width: 100%"><?= $contact_form_submit ?></button>
            </form>

          </div>
        </div>
      </div>
    </section>

<section class="leaders" id="leaders" aria-labelledby="leaders-title">
  <div class="leaders__main container">
    <header class="subtitle">
      <span class="subtitle__badge"><?= $leaders_badge ?></span>
      <h2 class="subtitle-h2" id="leaders-title"><?= $leaders_title ?></h2>
    </header>

    <div class="leaders__slider swiper mySwiper swiper-initialized swiper-horizontal swiper-backface-hidden">
      <div class="swiper-wrapper" id="swiper-wrapper-303dd2be8c11dd510" aria-live="polite">

        <div class="swiper-slide swiper-slide-active" role="group" aria-label="1 / 2" style="width: 1156px; margin-right: 30px;">
          <div class="leaders__card">
            <div class="leaders__text">
              <p class="leaders__description"><?= $leader1_text ?></p>
              <div class="leaders__info">
                <h3 class="leaders__info_name"><?= $leader1_name ?></h3>
                <small class="leaders__info_position"><?= $leader1_position ?></small>
              </div>
            </div>
            <div class="leaders__image">
              <img src="images/Warren_Buffett.webp" width="375" height="375" loading="lazy" alt="avatar">
              <span>
                <img class="leaders__image-coin visible-tablet" src="images/coin-2.webp" width="50" height="45" alt="Digital coin growth">
                <img class="leaders__image-coin" src="images/coin-3.webp" width="156" height="122" alt="Gold coin investment symbol">
                <img class="leaders__image-coin" src="images/coin-4.webp" width="82" height="69" alt="Financial coin market growth">
                <img class="leaders__image-coin" src="images/coin-5.webp" width="91" height="101" alt="Crypto investment AI trading">
              </span>
            </div>
          </div>
        </div>

        <div class="swiper-slide swiper-slide-next" role="group" aria-label="2 / 2" style="width: 1156px; margin-right: 30px;">
          <div class="leaders__card">
            <div class="leaders__text">
              <p class="leaders__description"><?= $leader2_text ?></p>
              <div class="leaders__info">
                <h3 class="leaders__info_name"><?= $leader2_name ?></h3>
                <small class="leaders__info_position"><?= $leader2_position ?></small>
              </div>
            </div>
            <div class="leaders__image">
              <img src="images/Larry_Fink.webp" width="375" height="375" alt="avatar" style="object-position: 64%;">
              <span>
                <img class="leaders__image-coin visible-tablet" src="images/coin-2.webp" width="50" height="45" alt="Digital coin growth">
                <img class="leaders__image-coin" src="images/coin-3.webp" width="156" height="122" alt="Gold coin investment symbol">
                <img class="leaders__image-coin" src="images/coin-4.webp" width="82" height="69" alt="Financial coin market growth">
                <img class="leaders__image-coin" src="images/coin-5.webp" width="91" height="101" alt="Crypto investment AI trading">
              </span>
            </div>
          </div>
        </div>

        <div class="swiper-slide swiper-slide-next" role="group" aria-label="2 / 2" style="width: 1156px; margin-right: 30px;">
          <div class="leaders__card">
            <div class="leaders__text">
              <p class="leaders__description"><?= $leader3_text ?></p>
              <div class="leaders__info">
                <h3 class="leaders__info_name"><?= $leader3_name ?></h3>
                <small class="leaders__info_position"><?= $leader3_position ?></small>
              </div>
            </div>
            <div class="leaders__image">
              <img src="images/Jamie_Dimon.webp" width="375" height="375" alt="avatar" style="object-position: 64%;">
              <span>
                <img class="leaders__image-coin visible-tablet" src="images/coin-2.webp" width="50" height="45" alt="Digital coin growth">
                <img class="leaders__image-coin" src="images/coin-3.webp" width="156" height="122" alt="Gold coin investment symbol">
                <img class="leaders__image-coin" src="images/coin-4.webp" width="82" height="69" alt="Financial coin market growth">
                <img class="leaders__image-coin" src="images/coin-5.webp" width="91" height="101" alt="Crypto investment AI trading">
              </span>
            </div>
          </div>
        </div>

      </div>

      <div class="swiper-buttons">
        <div class="swiper-button-prev leaders__slider-button swiper-button-disabled" tabindex="-1" role="button" aria-label="Previous slide" aria-controls="swiper-wrapper-303dd2be8c11dd510" aria-disabled="true">
          <img inert="" src="right-arrow.svg" alt="prev">
        </div>
        <div class="swiper-button-next leaders__slider-button" tabindex="0" role="button" aria-label="Next slide" aria-controls="swiper-wrapper-303dd2be8c11dd510" aria-disabled="false">
          <img inert="" src="right-arrow.svg" alt="next">
        </div>
      </div>

      <div class="swiper-pagination hidden-tablet swiper-pagination-clickable swiper-pagination-bullets swiper-pagination-horizontal">
        <span class="swiper-pagination-bullet swiper-pagination-bullet-active" tabindex="0" role="button" aria-label="Go to slide 1" aria-current="true"></span>
        <span class="swiper-pagination-bullet" tabindex="0" role="button" aria-label="Go to slide 2"></span>
      </div>

      <span class="swiper-notification" aria-live="assertive" aria-atomic="true"></span>
    </div>

    <span class="leaders__logo">
      <svg xmlns="http://www.w3.org/2000/svg" width="52" height="38" viewBox="0 0 52 38" fill="none"> <path d="M18.3364 14.0966L14.9802 17.4204C14.3396 18.0549 14.3396 19.0835 14.9802 19.718L18.6771 23.3792C19.3655 24.061 21.1066 23.4154 21.7951 22.7336L24.6495 19.9067C24.9571 19.602 25.1299 19.1888 25.1299 18.7579L25.1299 16.9812C25.1299 14.2894 27.3333 12.1073 30.0513 12.1073L34.8533 12.1073C37.5713 12.1073 39.7747 14.2894 39.7747 16.9812L39.7747 21.7368C39.7747 24.4286 37.5713 26.6107 34.8533 26.6107H33.0594C32.6243 26.6107 32.2071 26.7819 31.8994 27.0865L29.0449 29.9135C28.3565 30.5953 27.7046 32.3196 28.393 33.0014L32.0899 36.6626C32.7305 37.297 33.7692 37.297 34.4098 36.6626L37.977 33.1299C38.3999 32.711 38.5393 32.0988 38.4752 31.5099C38.3018 29.9167 38.8316 28.2627 40.0647 27.0415C41.2979 25.8203 42.968 25.2955 44.5766 25.4673C45.1713 25.5308 45.7895 25.3927 46.2124 24.9739L51.5195 19.718C52.1602 19.0835 52.1602 18.0549 51.5195 17.4204L46.7986 12.7451C46.3562 12.3069 45.7023 12.1788 45.0818 12.259C43.5575 12.456 41.9608 11.9747 40.7897 10.8149C39.6187 9.65514 39.1326 8.07386 39.3316 6.5642C39.4126 5.94971 39.2832 5.30218 38.8407 4.86398L34.4098 0.475842C33.7692 -0.158614 32.7305 -0.158614 32.0899 0.475843L26.9937 5.52281C26.5361 5.97603 26.4124 6.65078 26.5237 7.28217C26.8234 8.98185 26.3105 10.7946 24.985 12.1073C23.6595 13.42 21.8291 13.928 20.1129 13.6312C19.4753 13.5209 18.794 13.6434 18.3364 14.0966Z" fill="white"></path> <path d="M14.234 4.66122L17.5902 1.33743C18.2308 0.702975 19.2695 0.702974 19.9101 1.33743L23.607 4.99862C24.2954 5.68044 23.6435 7.40473 22.9551 8.08654L20.1007 10.9134C19.793 11.2181 19.3758 11.3892 18.9407 11.3892L17.1466 11.3892C14.4286 11.3892 12.2253 13.5713 12.2253 16.2631L12.2253 21.0188C12.2253 23.7105 14.4286 25.8926 17.1466 25.8926L21.9486 25.8926C24.6666 25.8926 26.87 23.7105 26.87 21.0188V19.2421C26.87 18.8113 27.0428 18.398 27.3505 18.0934L30.2049 15.2664C30.8934 14.5846 32.6345 13.939 33.3229 14.6208L37.0198 18.282C37.6604 18.9165 37.6604 19.9451 37.0198 20.5796L33.4527 24.1123C33.0298 24.5311 32.4115 24.6692 31.8169 24.6057C30.2082 24.4339 28.5381 24.9587 27.305 26.1799C26.0718 27.4011 25.542 29.0552 25.7154 30.6483C25.7796 31.2372 25.6401 31.8494 25.2172 32.2683L19.9101 37.5242C19.2695 38.1586 18.2308 38.1586 17.5902 37.5242L12.8693 32.8488C12.4268 32.4106 12.2974 31.7631 12.3784 31.1486C12.5774 29.6389 12.0914 28.0577 10.9203 26.8979C9.74922 25.7381 8.15253 25.2568 6.62816 25.4538C6.00768 25.534 5.35384 25.4059 4.91137 24.9677L0.480478 20.5796C-0.16016 19.9451 -0.160159 18.9165 0.480479 18.282L5.57662 13.235C6.03426 12.7818 6.71558 12.6593 7.35313 12.7696C9.06936 13.0664 10.8998 12.5584 12.2253 11.2457C13.5508 9.93299 14.0637 8.12026 13.764 6.42058C13.6526 5.78919 13.7763 5.11444 14.234 4.66122Z" fill="white"></path> </svg>
    </span>
  </div>
</section>

<section class="steps" id="steps" aria-labelledby="steps-title">
  <div class="steps__main container">
    <header class="subtitle">
      <span class="subtitle__badge"><?= $steps_badge ?></span>
      <h2 class="subtitle-h2" id="steps-title"><?= $steps_title ?></h2>
    </header>

    <div class="steps__content">
      <div class="steps__inner">

        <div class="steps__card">
          <div class="steps__card-header">
            <div class="steps__card-icon">
              <img src="images/icon-step-1.svg" width="36" height="36" alt="Sign up">
            </div>
            <small class="steps__card-number"><?= $step1_number ?></small>
          </div>
          <div class="steps__card-body">
            <h3 class="steps__card-title"><?= $step1_title ?></h3>
            <p class="steps__card-description"><?= $step1_text ?></p>
          </div>
        </div>

        <div class="steps__card">
          <div class="steps__card-header">
            <div class="steps__card-icon">
              <img src="images/icon-step-2.svg" width="36" height="36" alt="Invest">
            </div>
            <small class="steps__card-number"><?= $step2_number ?></small>
          </div>
          <div class="steps__card-body">
            <h3 class="steps__card-title"><?= $step2_title ?></h3>
            <p class="steps__card-description"><?= $step2_text ?></p>
          </div>
        </div>

        <div class="steps__card">
          <div class="steps__card-header">
            <div class="steps__card-icon">
              <img src="images/icon-step-3.svg" width="36" height="36" alt="Earn">
            </div>
            <small class="steps__card-number"><?= $step3_number ?></small>
          </div>
          <div class="steps__card-body">
            <h3 class="steps__card-title"><?= $step3_title ?></h3>
            <p class="steps__card-description"><?= $step3_text ?></p>
          </div>
        </div>

      </div>

      <a href="sign-up.php" class="steps__button button" data-js-button-form="">
        <?= $steps_button ?>
      </a>
    </div>
  </div>
</section>

<section class="trades" id="trades" aria-labelledby="trades-title">
  <div class="trades__main container">
    <header class="subtitle">
      <span class="subtitle__badge"><?= $trades_badge ?></span>
      <h2 class="subtitle-h2 max-w-600" id="trades-title">
        <?= $trades_title ?>
      </h2>
    </header>

    <div class="trades__card">
      <div class="trades__list">

        <div class="trades__item">
          <span class="trades__item-name"><?= $trade_btc_name ?></span>
          <span class="trades__item-value"><?= $trade_btc_value ?></span>
          <span class="trades__item-plus">
            <svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 36 36" fill="none">
              <rect width="36" height="36" rx="18" fill="#E3FF34"></rect>
              <path d="M18 26V18M18 10V18M18 18H10M18 18H26" stroke="#12393B"></path>
            </svg>
          </span>
        </div>

        <div class="trades__item">
          <span class="trades__item-name"><?= $trade_eth_name ?></span>
          <span class="trades__item-value"><?= $trade_eth_value ?></span>
          <span class="trades__item-plus">
            <svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 36 36" fill="none">
              <rect width="36" height="36" rx="18" fill="#E3FF34"></rect>
              <path d="M18 26V18M18 10V18M18 18H10M18 18H26" stroke="#12393B"></path>
            </svg>
          </span>
        </div>

        <div class="trades__item">
          <span class="trades__item-name"><?= $trade_ltc_name ?></span>
          <span class="trades__item-value"><?= $trade_ltc_value ?></span>
          <span class="trades__item-plus">
            <svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 36 36" fill="none">
              <rect width="36" height="36" rx="18" fill="#E3FF34"></rect>
              <path d="M18 26V18M18 10V18M18 18H10M18 18H26" stroke="#12393B"></path>
            </svg>
          </span>
        </div>

        <div class="trades__item">
          <span class="trades__item-name"><?= $trade_eos_name ?></span>
          <span class="trades__item-value"><?= $trade_eos_value ?></span>
          <span class="trades__item-plus">
            <svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 36 36" fill="none">
              <rect width="36" height="36" rx="18" fill="#E3FF34"></rect>
              <path d="M18 26V18M18 10V18M18 18H10M18 18H26" stroke="#12393B"></path>
            </svg>
          </span>
        </div>

        <div class="trades__item">
          <span class="trades__item-name"><?= $trade_xrp_name ?></span>
          <span class="trades__item-value"><?= $trade_xrp_value ?></span>
          <span class="trades__item-plus">
            <svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 36 36" fill="none">
              <rect width="36" height="36" rx="18" fill="#E3FF34"></rect>
              <path d="M18 26V18M18 10V18M18 18H10M18 18H26" stroke="#12393B"></path>
            </svg>
          </span>
        </div>

      </div>

      <div class="trades__image">
        <img src="images/laptop.webp" width="490" height="395" alt="laptop">
        <span>
          <img class="trades__image-coin visible-tablet" src="images/coin-2.webp" width="50" height="45" alt="Digital coin growth">
          <img class="trades__image-coin" src="images/coin-3.webp" width="156" height="122" alt="Gold coin investment symbol">
          <img class="trades__image-coin" src="images/coin-4.webp" width="82" height="69" alt="Financial coin market growth">
          <img class="trades__image-coin" src="images/coin-5.webp" width="91" height="101" alt="Crypto investment AI trading">
          <img class="trades__image-coin visible-tablet" src="images/coin-6.webp" width="58" height="46" alt="AI trading coin concept">
        </span>
      </div>

    </div>
  </div>
</section>

<section class="advantages" id="advantages" aria-labelledby="advantages-title">
  <div class="advantages__main container">
    <header class="subtitle">
      <span class="subtitle__badge"><?= $advantages_badge ?></span>
      <h2 class="subtitle-h2 max-w-600" id="advantages-title">
        <?= $advantages_title ?>
      </h2>
    </header>

    <div class="advantages__swiper" data-js-swiper="">
      <div class="advantages__inner" data-js-swiper-inner="">

        <div class="advantages__card" data-js-swiper-card="">
          <div class="advantages__card-text">
            <span class="advantages__card-badge"><?= $advantages_card_badge ?></span>
            <div class="advantages__card-body">
              <h3 class="advantages__card-title"><?= $adv1_title ?></h3>
              <p class="advantages__card-description">
                <?= $adv1_text ?>
              </p>
            </div>
          </div>
          <div class="advantages__card-image">
            <span class="advantages__card-picture" role="img" aria-label="Easy to use"></span>
            <span class="advantages__card-icon">
              <img src="images/icon-advantages-1.webp" width="48" height="48" alt="icon">
            </span>
          </div>
        </div>

        <div class="advantages__card" data-js-swiper-card="">
          <div class="advantages__card-text">
            <span class="advantages__card-badge"><?= $advantages_card_badge ?></span>
            <div class="advantages__card-body">
              <h3 class="advantages__card-title"><?= $adv2_title ?></h3>
              <p class="advantages__card-description">
                <?= $adv2_text ?>
              </p>
            </div>
          </div>
          <div class="advantages__card-image">
            <span class="advantages__card-picture" role="img" aria-label="Trusted Performance"></span>
            <span class="advantages__card-icon">
              <img src="images/icon-advantages-2.webp" width="48" height="48" alt="icon">
            </span>
          </div>
        </div>

        <div class="advantages__card" data-js-swiper-card="">
          <div class="advantages__card-text">
            <span class="advantages__card-badge"><?= $advantages_card_badge ?></span>
            <div class="advantages__card-body">
              <h3 class="advantages__card-title"><?= $adv3_title ?></h3>
              <p class="advantages__card-description">
                <?= $adv3_text ?>
              </p>
            </div>
          </div>
          <div class="advantages__card-image">
            <span class="advantages__card-picture" role="img" aria-label="Secure & Private"></span>
            <span class="advantages__card-icon">
              <img src="images/icon-advantages-3.webp" width="48" height="48" alt="icon">
            </span>
          </div>
        </div>

      </div>

      <div class="pagination-swiper visible-tablet">
        <div class="pagination-swiper-dot pagination-swiper-dot--active"></div>
        <div class="pagination-swiper-dot"></div>
        <div class="pagination-swiper-dot"></div>
      </div>
    </div>
  </div>
</section>

<section class="statistics" id="statistics" aria-labelledby="statistics-title">
  <div class="statistics__main container">
    <header class="subtitle">
      <span class="subtitle__badge"><?= $statistics_badge ?></span>
      <h2 class="subtitle-h2" id="statistics-title"><?= $statistics_title ?></h2>

      <p class="statistics__description max-w-730">
        <?= $statistics_description_top ?>
      </p>
    </header>

    <div class="statistics__content">
      <div class="statistics__inner">

        <div class="statistics__card">
          <div class="statistics__card-header">
            <span class="statistics__card-value" style="white-space: nowrap" data-js-deposit-multiply-bignumber-noword="6"><?= $stat1_value ?></span>
            <p class="statistics__card-denomination"><?= $stat1_denomination ?></p>
          </div>
          <div class="statistics__card-title"><?= $stat1_title ?></div>
        </div>

        <div class="statistics__card">
          <div class="statistics__card-header">
            <span class="statistics__card-value" style="white-space: nowrap" data-js-deposit-multiply-bignumber-noword="346000"><?= $stat2_value ?></span>
            <p class="statistics__card-denomination"><?= $stat2_denomination ?></p>
          </div>
          <div class="statistics__card-title"><?= $stat2_title ?></div>
        </div>

        <div class="statistics__card">
          <div class="statistics__card-header">
            <span class="statistics__card-value" style="white-space: nowrap" data-js-deposit-multiply-bignumber-noword="1181.6"><?= $stat3_value ?></span>
            <p class="statistics__card-denomination"><?= $stat3_denomination ?></p>
          </div>
          <div class="statistics__card-title"><?= $stat3_title ?></div>
        </div>

      </div>

      <p class="statistics__description statistics__description-bottom">
        <?= $statistics_description_bottom ?>
      </p>
    </div>
  </div>
</section>

    <section class="feedback" id="feedback" aria-labelledby="feedback-title">
      <div class="feedback__main container">
        <header class="subtitle">
          <span class="subtitle__badge"> <?= $feedback ?> </span>
          <h2 class="subtitle-h2" id="feedback-title"> <?= $recommendations ?> </h2>
        </header>
        <div class="feedback__swiper" data-js-swiper="">
          <div class="feedback__list" data-js-swiper-inner="">
            <article class="feedback__item" data-js-swiper-card="">
              <header class="feedback__header">
                <div class="feedback__header-avatar">
                  <img style="object-position: top" src="images/feedback-1.webp" width="100" height="100" loading="lazy" alt="Avatar">
                </div>
                <div class="feedback__header-info">
                  <span class="feedback__header-name"><?= $feedback_strong_1 ?></span>
                  <span class="feedback__header-value" style="white-space: nowrap" data-js-deposit-multiply="93.202">23.312,53 €</span>
                </div>
              </header>
              <p class="feedback__decription">
                <?= $feedback_description_1 ?>
              </p>
            </article>
            <article class="feedback__item" data-js-swiper-card="">
              <header class="feedback__header">
                <div class="feedback__header-avatar">
                  <img src="images/feedback-2.webp" width="100" height="100" loading="lazy" alt="Avatar">
                </div>
                <div class="feedback__header-info">
                  <span class="feedback__header-name"><?= $feedback_strong_2 ?></span>
                  <span class="feedback__header-value" style="white-space: nowrap" data-js-deposit-multiply="72.185">18.054,94 €</span>
                </div>
              </header>
              <p class="feedback__decription">
                <?= $feedback_description_2 ?>
              </p>
            </article>
            <article class="feedback__item" data-js-swiper-card="">
              <header class="feedback__header">
                <div class="feedback__header-avatar no-avatar">
                  <img src="images/feedback-3.webp" width="100" height="100" loading="lazy" alt="Avatar" style="object-position: top;">
                  <!-- <span>MA</span> -->
                </div>
                <div class="feedback__header-info">
                  <span class="feedback__header-name"><?= $feedback_strong_3 ?></span>
                  <span class="feedback__header-value" style="white-space: nowrap" data-js-deposit-multiply="15.64">3.911,92 €</span>
                </div>
              </header>
              <p class="feedback__decription">
                <?= $feedback_description_3 ?>
              </p>
            </article>
            <article class="feedback__item" data-js-swiper-card="">
              <header class="feedback__header">
                <div class="feedback__header-avatar no-avatar">
                  <img src="images/feedback-4.webp" width="100" height="100" loading="lazy" alt="Avatar">
                  <!-- <span>SA</span> -->
                </div>
                <div class="feedback__header-info">
                  <span class="feedback__header-name"><?= $feedback_strong_4 ?></span>
                  <span class="feedback__header-value" style="white-space: nowrap" data-js-deposit-multiply="35.7">8.929,43 €</span>
                </div>
              </header>
              <p class="feedback__decription">
                <?= $feedback_description_4 ?>
              </p>
            </article>
            <article class="feedback__item" data-js-swiper-card="">
              <header class="feedback__header">
                <div class="feedback__header-avatar">
                  <img src="images/feedback-5.webp" width="100" height="100" loading="lazy" alt="Avatar">
                </div>
                <div class="feedback__header-info">
                  <span class="feedback__header-name"><?= $feedback_strong_5 ?></span>
                  <span class="feedback__header-value" style="white-space: nowrap" data-js-deposit-multiply="102.334">25.596,69 €</span>
                </div>
              </header>
              <p class="feedback__decription">
                <?= $feedback_description_5 ?>
              </p>
            </article>
            <article class="feedback__item" data-js-swiper-card="">
              <header class="feedback__header">
                <div class="feedback__header-avatar">
                  <img src="images/feedback-6.webp" width="100" height="100" loading="lazy" alt="Avatar">
                </div>
                <div class="feedback__header-info">
                  <span class="feedback__header-name"><?= $feedback_strong_6 ?></span>
                  <span class="feedback__header-value" style="white-space: nowrap" data-js-deposit-multiply="57.155">14.296,08 €</span>
                </div>
              </header>
              <p class="feedback__decription">
                <?= $feedback_description_6 ?>
              </p>
            </article>
          </div>
          <div class="pagination-swiper visible-tablet">
            <div class="pagination-swiper-dot pagination-swiper-dot--active"></div>
            <div class="pagination-swiper-dot"></div>
            <div class="pagination-swiper-dot"></div>
            <div class="pagination-swiper-dot"></div>
            <div class="pagination-swiper-dot"></div>
            <div class="pagination-swiper-dot"></div>
          </div>
        </div>
      </div>
    </section>

    <section class="join" aria-labelledby="join-title">
      <div class="join__main container">
<div class="join__text">
  <span class="join__title" id="join-title">
    <span><?= $join_title_main ?></span>
    <a class="join__block" href="" aria-label="Logo" title="Logo">
      <span class="join__title-accent"><?= $join_title_accent ?></span>

      <span class="join__logo logo">
        <svg xmlns="http://www.w3.org/2000/svg" width="40" height="30" viewBox="0 0 40 30" fill="none">
          <path d="M13.7943 11.3128L11.2695 13.8133C10.7876 14.2906 10.7876 15.0644 11.2695 15.5417L14.0506 18.296C14.5686 18.8089 15.8784 18.3232 16.3963 17.8103L18.5436 15.6837C18.7751 15.4545 18.9051 15.1436 18.9051 14.8195L18.9051 13.4828C18.9051 11.4578 20.5627 9.81625 22.6074 9.81625H26.2199C28.2646 9.81625 29.9222 11.4578 29.9222 13.4828L29.9222 17.0605C29.9222 19.0855 28.2646 20.7271 26.2199 20.7271H24.8704C24.5431 20.7271 24.2292 20.8558 23.9977 21.085L21.8503 23.2117C21.3324 23.7246 20.842 25.0218 21.3599 25.5347L24.141 28.289C24.623 28.7663 25.4044 28.7663 25.8863 28.289L28.5698 25.6314C28.888 25.3163 28.9929 24.8557 28.9446 24.4127C28.8142 23.2142 29.2128 21.9699 30.1404 21.0512C31.0681 20.1324 32.3245 19.7377 33.5347 19.8669C33.9821 19.9147 34.4472 19.8108 34.7653 19.4957L38.7578 15.5417C39.2398 15.0644 39.2398 14.2906 38.7578 13.8133L35.2063 10.2961C34.8734 9.96641 34.3816 9.87003 33.9148 9.93037C32.768 10.0786 31.5668 9.71648 30.6858 8.84399C29.8049 7.97151 29.4392 6.78192 29.5889 5.64622C29.6498 5.18394 29.5525 4.6968 29.2196 4.36715L25.8863 1.06598C25.4044 0.588683 24.623 0.588684 24.141 1.06598L20.3072 4.86278C19.9629 5.20374 19.8699 5.71135 19.9536 6.18634C20.1791 7.465 19.7932 8.8287 18.7961 9.81625C17.7989 10.8038 16.4219 11.1859 15.1308 10.9626C14.6512 10.8797 14.1386 10.9719 13.7943 11.3128Z" fill="#E3FF34"></path>
          <path d="M10.7081 4.21461L13.233 1.71415C13.7149 1.23685 14.4963 1.23685 14.9783 1.71415L17.7594 4.46844C18.2773 4.98137 17.7869 6.27854 17.2689 6.79146L15.1216 8.91808C14.8902 9.14728 14.5763 9.27605 14.249 9.27605H12.8993C10.8546 9.27605 9.19699 10.9176 9.19699 12.9426L9.19698 16.5203C9.19698 18.5453 10.8546 20.1869 12.8993 20.1869L16.5118 20.1869C18.5565 20.1869 20.2141 18.5453 20.2141 16.5203V15.1838C20.2141 14.8596 20.3441 14.5487 20.5756 14.3195L22.723 12.1929C23.2409 11.6799 24.5507 11.1942 25.0686 11.7072L27.8498 14.4614C28.3317 14.9387 28.3317 15.7126 27.8498 16.1899L25.1662 18.8475C24.8481 19.1626 24.383 19.2665 23.9356 19.2187C22.7255 19.0895 21.469 19.4843 20.5414 20.403C19.6137 21.3217 19.2151 22.566 19.3456 23.7645C19.3938 24.2075 19.2889 24.6681 18.9707 24.9832L14.9782 28.9372C14.4963 29.4145 13.7149 29.4145 13.233 28.9372L9.68147 25.42C9.3486 25.0903 9.25129 24.6032 9.31222 24.1409C9.4619 23.0052 9.09624 21.8156 8.21526 20.9431C7.33427 20.0706 6.1331 19.7085 4.98632 19.8567C4.51954 19.9171 4.02766 19.8207 3.69479 19.4911L0.361461 16.1899C-0.120487 15.7126 -0.120487 14.9387 0.361461 14.4614L4.19526 10.6646C4.53953 10.3237 5.05209 10.2315 5.53171 10.3145C6.82282 10.5378 8.19981 10.1556 9.19698 9.16808C10.1942 8.18053 10.58 6.81683 10.3546 5.53817C10.2708 5.06318 10.3639 4.55557 10.7081 4.21461Z" fill="#E3FF34"></path>
        </svg>
        <span><?= $source ?></span>
      </span>
    </a>
  </span>
</div>
        <div class="join__form">
          <div class="form" data-js-form="">
            <style>
              .iti__selected-dial-code,
              .iti__country-name {
                color: black;
              }

              .leadform {
                max-width: 400px;
                margin: 0 auto;
              }

              .leadform input {
                display: block;
                width: 100%;
                border-radius: 5px;
                border: 1px solid #ccc;
                margin: 20px 0;
                padding: 15px;
              }

              .submit {
                animation: 2s ease 0s infinite normal none running aio-sdk-pulsing;
                box-shadow: #12393b 0 0 0 0;
                background: #12393b;
                border-color: #12393b;
                color: #e3ff34;
                padding: 12px;
                height: 60px;
                border: 1px solid transparent;
                border-radius: 50px;
                margin-top: 20px;
                text-transform: uppercase;
                font-weight: 400;
                font-size: 16px;

                transition: 50ms ease-out;

                outline: 0;
                box-sizing: border-box;
                position: relative;
                cursor: pointer;
                width: 100%;

              }

              @keyframes aio-sdk-pulsing {
                100% {
                  box-shadow: transparent 0 0 0 10px
                }
              }
            </style>

            <form class="leadform rf-form js-rf-form" id="form2" method="post" action="./integration/send.php">
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
                <circle class="path" cx="25" cy="25" r="20" fill="none"   stroke-width="5"></circle>
            </svg>
            </div>

            <input type="text" placeholder="<?= $contact_form_fname ?>" name="fname" required="">
            <input type="text" placeholder="<?= $contact_form_lname ?>" name="lname" required="">
            <input type="email" placeholder="<?= $contact_form_email ?>" name="email" required="">
            <input type="tel" name="fullphone" required="">
            <span class="error-msg hide"></span>
            <button type="submit" class="submit" style="width: 100%"><?= $contact_form_submit ?></button>
            </form>

          </div>
        </div>
      </div>
    </section>

<footer class="footer container">
  <div class="footer__main">
    <div class="footer__top">
      <a class="footer__logo logo" href="" aria-label="Footer" title="Footer">
        <svg xmlns="http://www.w3.org/2000/svg" width="40" height="30" viewBox="0 0 40 30" fill="none">
          <path d="M13.7943 11.3128L11.2695 13.8133C10.7876 14.2906 10.7876 15.0644 11.2695 15.5417L14.0506 18.296C14.5686 18.8089 15.8784 18.3232 16.3963 17.8103L18.5436 15.6837C18.7751 15.4545 18.9051 15.1436 18.9051 14.8195L18.9051 13.4828C18.9051 11.4578 20.5627 9.81625 22.6074 9.81625H26.2199C28.2646 9.81625 29.9222 11.4578 29.9222 13.4828L29.9222 17.0605C29.9222 19.0855 28.2646 20.7271 26.2199 20.7271H24.8704C24.5431 20.7271 24.2292 20.8558 23.9977 21.085L21.8503 23.2117C21.3324 23.7246 20.842 25.0218 21.3599 25.5347L24.141 28.289C24.623 28.7663 25.4044 28.7663 25.8863 28.289L28.5698 25.6314C28.888 25.3163 28.9929 24.8557 28.9446 24.4127C28.8142 23.2142 29.2128 21.9699 30.1404 21.0512C31.0681 20.1324 32.3245 19.7377 33.5347 19.8669C33.9821 19.9147 34.4472 19.8108 34.7653 19.4957L38.7578 15.5417C39.2398 15.0644 39.2398 14.2906 38.7578 13.8133L35.2063 10.2961C34.8734 9.96641 34.3816 9.87003 33.9148 9.93037C32.768 10.0786 31.5668 9.71648 30.6858 8.84399C29.8049 7.97151 29.4392 6.78192 29.5889 5.64622C29.6498 5.18394 29.5525 4.6968 29.2196 4.36715L25.8863 1.06598C25.4044 0.588683 24.623 0.588684 24.141 1.06598L20.3072 4.86278C19.9629 5.20374 19.8699 5.71135 19.9536 6.18634C20.1791 7.465 19.7932 8.8287 18.7961 9.81625C17.7989 10.8038 16.4219 11.1859 15.1308 10.9626C14.6512 10.8797 14.1386 10.9719 13.7943 11.3128Z" fill="#E3FF34"></path>
          <path d="M10.7081 4.21461L13.233 1.71415C13.7149 1.23685 14.4963 1.23685 14.9783 1.71415L17.7594 4.46844C18.2773 4.98137 17.7869 6.27854 17.2689 6.79146L15.1216 8.91808C14.8902 9.14728 14.5763 9.27605 14.249 9.27605H12.8993C10.8546 9.27605 9.19699 10.9176 9.19699 12.9426L9.19698 16.5203C9.19698 18.5453 10.8546 20.1869 12.8993 20.1869L16.5118 20.1869C18.5565 20.1869 20.2141 18.5453 20.2141 16.5203V15.1838C20.2141 14.8596 20.3441 14.5487 20.5756 14.3195L22.723 12.1929C23.2409 11.6799 24.5507 11.1942 25.0686 11.7072L27.8498 14.4614C28.3317 14.9387 28.3317 15.7126 27.8498 16.1899L25.1662 18.8475C24.8481 19.1626 24.383 19.2665 23.9356 19.2187C22.7255 19.0895 21.469 19.4843 20.5414 20.403C19.6137 21.3217 19.2151 22.566 19.3456 23.7645C19.3938 24.2075 19.2889 24.6681 18.9707 24.9832L14.9782 28.9372C14.4963 29.4145 13.7149 29.4145 13.233 28.9372L9.68147 25.42C9.3486 25.0903 9.25129 24.6032 9.31222 24.1409C9.4619 23.0052 9.09624 21.8156 8.21526 20.9431C7.33427 20.0706 6.1331 19.7085 4.98632 19.8567C4.51954 19.9171 4.02766 19.8207 3.69479 19.4911L0.361461 16.1899C-0.120487 15.7126 -0.120487 14.9387 0.361461 14.4614L4.19526 10.6646C4.53953 10.3237 5.05209 10.2315 5.53171 10.3145C6.82282 10.5378 8.19981 10.1556 9.19698 9.16808C10.1942 8.18053 10.58 6.81683 10.3546 5.53817C10.2708 5.06318 10.3639 4.55557 10.7081 4.21461Z" fill="#E3FF34"></path>
        </svg>
        <span><?= $source ?></span>
      </a>

      <style>
        .footer__button.button {
          color: var(--color-emerald-12);
          background: #d0ee11;
        }
      </style>

      <a href="sign-up.php" class="footer__button button" data-js-button-form="">
        <?= $button_register ?>
      </a>

      <ul class="footer__nav">
        <li class="footer__nav-item"><a href="about-us.php" class="no-scroll"><?= $footer_about ?></a></li>
        <li class="footer__nav-item"><a href="contact.php" class="no-scroll"><?= $footer_contact ?></a></li>
        <li class="footer__nav-item"><a href="sign-up.php" class="no-scroll"><?= $footer_registration ?></a></li>
        <li class="footer__nav-item"><a href="conditions.php" class="no-scroll"><?= $footer_terms ?></a></li>
        <li class="footer__nav-item"><a href="private-policy.php" class="no-scroll"><?= $footer_privacy ?></a></li>
      </ul>
    </div>

    <div class="footer__bottom">
      <span>
        <?= $footer_rights ?>
        <span class="visible-tablet" data-current-year="">2026</span>
      </span>
      <span class="hidden-tablet" data-current-year="">2026</span>
    </div>
  </div>
</footer>

<dialog class="places" data-js-dialog="">
  <div class="places__main container">
    <div class="places__title hidden-tablet">
      <div class="places__image">
        <img src="images/pntro.png" width="40" height="40" alt="flag">
      </div>
      <h2 class="places__text">
        <?= $places_title ?>
      </h2>
    </div>

    <div class="places__body">
      <div class="places__remaining">
        <span class="places__remaining-text"><?= $places_remaining_text ?></span>
        <span class="places__remaining-number" data-js-places-remaining=""></span>
      </div>

      <button class="places__button button" type="button" data-js-button-form="">
        <?= $places_button ?>
      </button>
    </div>
  </div>
</dialog>
  </main>
  <style>
    .aio-sdk-form {
      --aio-sdk-input-border-radius: 8px;
      --aio-sdk-input-padding: 12px;
      --aio-sdk-form-padding: 40px;
      --aio-sdk-input-margin: 20px;
      --aio-sdk-submit-bg: #e3ff34;
      --aio-sdk-submit-border-radius: 50px;
      --aio-sdk-submit-color: #12393b;
      --aio-sdk-submit-font-size: 16px;
      --aio-sdk-input-label-margin: 8px;
    }

    .aio-sdk-form button[type='submit'] {
      font-weight: 500;
      height: 60px;
    }

    .aio-sdk-form button[type='submit']:hover {
      background: #d0ee11;
    }

    .aio-sdk-form .aio-sdk-input-container:last-child {
      padding-top: 4px;
      margin-bottom: 0;
    }

    .aio-sdk-input-container::before {
      color: #999999;
      font-size: 16px;
      font-style: normal;
      font-weight: 500;
      line-height: 140%;
      display: block;
      content: '';
    }

    .itit-aio__flag-box,
    .itit-aio__country-name {
      color: #222222;
    }

    .itit-aio__search-input {
      border-radius: 8px;
    }

    .itit-aio--inline-dropdown .itit-aio__dropdown-content {
      box-shadow: none;
      border-radius: 8px;
      border: 1px solid #ccc;
    }

    .aio-sdk-input::placeholder {
      color: #bbbbbb;
    }

    .itit-aio__country-list::-webkit-scrollbar {
      width: 4px;
      height: 4px;
    }

    .itit-aio__country-list::-webkit-scrollbar-thumb {
      border-radius: 10px;
      background: #ddd;
    }

    .itit-aio__country-list::-webkit-scrollbar-track {
      background: transparent;
    }

    @media (max-width: 1024px) {
      .aio-sdk-form {
        --aio-sdk-submit-border-radius: 60px;
        --aio-sdk-submit-bg: #12393b;
        --aio-sdk-submit-color: #e3ff34;
      }

      .aio-sdk-form .aio-sdk-input-container:last-child {
        padding-top: 4px;
      }

      .aio-sdk-form button[type='submit']:hover {
        background: #e3ff34;
        color: #12393b;
      }
    }

    .join__title-accent {
      white-space: nowrap;
    }

    .join__block {
      flex-wrap: wrap;
    }

    @media (max-width: 500px) {
      .join__block {
        display: flex;
        flex-direction: column;
        gap: 10px;
        justify-content: center;
      }
    }
  </style>

  <style>
    .custom-dropdown-wrapper {
      position: relative;
      width: 100%;
    }

    .custom-dropdown-selected {
      padding-right: 32px !important;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
      cursor: pointer;
      height: auto;
      box-sizing: border-box;
      font-size: 17px !important;
    }

    .custom-dropdown-arrow {
      position: absolute;
      right: 12px;
      top: 50%;
      transform: translateY(-50%);
      pointer-events: none;
      font-size: 14px;
      color: #555;
      line-height: 1;
      height: 1em;
      display: flex;
      align-items: center;
    }

    .custom-dropdown-list {
      position: absolute;
      top: 100%;
      left: 0;
      right: 0;
      background: white;
      border-radius: 8px;
      border: 1px solid #ccc;
      margin-top: 4px;
      max-height: 160px;
      overflow-y: auto;
      display: none;
      z-index: 100;
      box-shadow: 0 4px 8px rgba(0, 0, 0, 0.08);
      padding: 0;
      list-style: none;
    }

    .custom-dropdown-list::-webkit-scrollbar {
      width: 4px;
    }

    .custom-dropdown-list::-webkit-scrollbar-thumb {
      border-radius: 10px;
      background: #ddd;
    }

    .custom-dropdown-option {
      padding: 12px;
      cursor: pointer;
      transition: background 0.2s ease;
    }

    .custom-dropdown-option:hover {
      background: #f2f2f2;
    }

    .custom-dropdown-option {
      padding: 12px;
      cursor: pointer;
      transition: background 0.2s ease;
      /* Совпадает с .itit-aio__flag-box и .itit-aio__country-name */
      color: #222222;
      font-size: 16px;
      font-weight: 400;
      font-family: inherit;
    }

    input.custom-dropdown-selected::placeholder {
      font-size: 14px !important;
    }

    @media (max-width: 1200px) {
      input.custom-dropdown-selected::placeholder {
        font-size: 13px !important;
      }

      .custom-dropdown-selected {
        font-size: 13px !important;
      }
    }

    @media (max-width: 991px) {
      input.custom-dropdown-selected::placeholder {
        font-size: 12px !important;
      }

      .custom-dropdown-selected {
        font-size: 12px !important;
      }
    }
  </style>

  <style>
    /* Enhanced mobile styles for leaders slider */
    @media (max-width: 768px) {
      .leaders__slider {
        margin-block: 2rem 3rem;
        overflow: hidden;
        width: 100%;
      }

      .leaders__slider .swiper-wrapper {
        /* Let Swiper handle all positioning */
        display: flex;
        align-items: center;
      }

      .leaders__slider .swiper-slide {
        /* Ensure slides take full width and are centered */
        width: 100%;
        max-width: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
        flex-shrink: 0;
      }

      .leaders__card {
        padding: 1rem;
        text-align: center;
        width: 100%;
        max-width: 100%;
        margin: 0 auto;
        display: flex;
        flex-direction: column-reverse;
        align-items: center;
      }

      .leaders__text {
        margin-bottom: 2rem;
        width: 100%;
      }

      .leaders__description {
        font-size: 1rem;
        line-height: 1.5;
        margin-bottom: 1.5rem;
      }

      .leaders__info {
        align-items: center;
        text-align: center;
      }

      .leaders__image {
        margin-bottom: 1rem;
      }

      .leaders__image>img {
        width: 15rem;
        height: 15rem;
        margin: 0 auto 2rem auto;
      }

      /* Hide navigation buttons on mobile and show pagination */
      .swiper-buttons {
        display: none !important;
      }

      .leaders__slider .swiper-pagination {
        display: block !important;
        position: static;
        margin-top: 1.5rem;
      }

      .leaders__slider .swiper-pagination-bullet {
        width: 12px;
        height: 12px;
        background: transparent;
        border: 2px solid var(--color-accent);
        opacity: 0.5;
        margin: 0 6px;
      }

      .leaders__slider .swiper-pagination-bullet-active {
        background: var(--color-accent);
        opacity: 1;
      }

      /* Make slides full width on mobile */
      .leaders__slider .swiper-slide {
        width: 100% !important;
        margin-right: 0 !important;
      }

      .leaders__slider .swiper-wrapper {
        display: flex;
      }

      /* Improve coin positioning on mobile */
      .leaders__image-coin {
        z-index: 1;
      }

      .leaders__image-coin:nth-child(1) {
        width: 2.5rem;
        height: 2.5rem;
        right: -1rem;
        top: 10%;
      }

      .leaders__image-coin:nth-child(2) {
        width: 4rem;
        height: 3rem;
        right: -0.5rem;
        bottom: 1rem;
      }

      .leaders__image-coin:nth-child(3) {
        width: 2rem;
        height: 1.5rem;
        top: -0.5rem;
        right: 1rem;
      }

      .leaders__image-coin:nth-child(4) {
        width: 2.5rem;
        height: 2.5rem;
        left: -1rem;
        top: 1rem;
      }
    }

    /* Enhanced styles for tablets */
    @media (min-width: 769px) and (max-width: 1024px) {
      .leaders__slider .swiper-buttons {
        display: flex;
      }

      .leaders__slider .swiper-pagination {
        display: none;
      }
    }

    /* Enhanced desktop styles */
    @media (min-width: 1025px) {
      .leaders__slider .swiper-buttons {
        display: flex;
      }

      .leaders__slider .swiper-pagination {
        display: none;
      }
    }

    /* Touch-friendly navigation */
    .leaders__slider .swiper-pagination-bullet {
      cursor: pointer;
      transition: all 0.3s ease;
    }

    .leaders__slider .swiper-pagination-bullet:hover {
      transform: scale(1.2);
    }

    /* Smooth transitions */
    .leaders__slider .swiper-slide {
      transition: transform 0.3s ease;
    }

    .leaders__slider .swiper-slide-active .leaders__card {
      animation: slideInContent 0.6s ease-out;
    }

    @keyframes slideInContent {
      from {
        opacity: 0;
        transform: translateY(20px);
      }

      to {
        opacity: 1;
        transform: translateY(0);
      }
    }

    /* Enhanced autoplay indicator */
    .leaders__slider .swiper-pagination-bullet {
      transition: all 0.3s ease;
      background: rgba(255, 255, 255, 0.5);
    }

    .leaders__slider .swiper-pagination-bullet-active {
      background: #E3FF34;
      transform: scale(1.2);
    }

    /* Ensure proper spacing and centering */
    .leaders__slider .swiper-container {
      padding-bottom: 2rem;
    }
  </style>

  <script src="js/swiper-bundle.min.js"></script>




  <script>
    // Initialize Swiper for leaders section
    document.addEventListener('DOMContentLoaded', function() {
      const leadersSwiper = new Swiper('.leaders__slider', {
        slidesPerView: 1,
        spaceBetween: 0,
        loop: true,
        speed: 800,
        autoplay: {
          delay: 5000,
          disableOnInteraction: false,
        },
        navigation: {
          nextEl: '.leaders__slider .swiper-button-next',
          prevEl: '.leaders__slider .swiper-button-prev',
        },
        pagination: {
          el: '.leaders__slider .swiper-pagination',
          clickable: true,
        },
        breakpoints: {
          320: {
            slidesPerView: 1,
            spaceBetween: 0,
          },
          768: {
            slidesPerView: 1,
            spaceBetween: 0,
          },
          1024: {
            slidesPerView: 1,
            spaceBetween: 0,
          }
        }
      });

      // Initialize other swipers (advantages and feedback sections)
      const advantagesSwiper = new Swiper('.advantages__swiper', {
        slidesPerView: 1,
        spaceBetween: 20,
        pagination: {
          el: '.advantages__swiper .pagination-swiper',
          clickable: true,
          renderBullet: function(index, className) {
            return '<div class="' + className + ' pagination-swiper-dot"></div>';
          },
        },
        breakpoints: {
          768: {
            slidesPerView: 2,
            spaceBetween: 30,
          },
          1024: {
            slidesPerView: 3,
            spaceBetween: 30,
          }
        }
      });

      const feedbackSwiper = new Swiper('.feedback__swiper', {
        slidesPerView: 1,
        spaceBetween: 20,
        pagination: {
          el: '.feedback__swiper .pagination-swiper',
          clickable: true,
          renderBullet: function(index, className) {
            return '<div class="' + className + ' pagination-swiper-dot"></div>';
          },
        },
        breakpoints: {
          768: {
            slidesPerView: 2,
            spaceBetween: 30,
          },
          1024: {
            slidesPerView: 3,
            spaceBetween: 30,
          }
        }
      });
    });
  </script>

  <script src="https://cdn.jsdelivr.net/npm/intl-tel-input@23.0.12/build/js/intlTelInput.min.js"></script>
  <script src="./integration/validation.js"></script>


<script>
let links = document.querySelectorAll('a');
let form = document.querySelector('#form2');

links.forEach((el) => {
    el.addEventListener('click', (e) => {

        let href = el.getAttribute('href');

        if (!href || href === "#" || href.trim() === "") {
            e.preventDefault();

            form.scrollIntoView({
                behavior: 'smooth',
                block: 'center'
            });
        }

    });
});
</script>

<script>
document.addEventListener("DOMContentLoaded", () => {

  const burger = document.querySelector('[data-js-header-burger-button]');
  const overlay = document.querySelector('[data-js-header-overlay]');
  const backdrop = document.querySelector('.backdrop');
  const menuLinks = document.querySelectorAll('.header__menu-link');
  const menuButton = document.querySelector('[data-js-button-form]');

  function closeMenu() {
    burger.classList.remove('is-active');
    overlay.classList.remove('is-active');
    backdrop.classList.remove('is-active');
    document.body.classList.remove('menu-open');
  }

  function toggleMenu() {
    burger.classList.toggle('is-active');
    overlay.classList.toggle('is-active');
    backdrop.classList.toggle('is-active');
    document.body.classList.toggle('menu-open');
  }

  burger.addEventListener('click', toggleMenu);
  backdrop.addEventListener('click', closeMenu);

  menuLinks.forEach(link => {
    link.addEventListener('click', closeMenu);
  });

  if (menuButton) {
    menuButton.addEventListener('click', closeMenu);
  }

});
</script>

</body>

</html>
