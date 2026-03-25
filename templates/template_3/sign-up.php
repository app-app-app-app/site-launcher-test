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
  <link rel="shortcut icon" href="favicon.svg" type="image/x-icon">
  <title><?= $page_title_register ?></title>
  <meta name="description" content="<?= $page_description_register ?>">
  <link rel="stylesheet" href="css/swiper-bundle.min.css">
  <link rel="stylesheet" href="css/main-1.css">

  <link rel="stylesheet" media="all" href="css/main.css">
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
        <style>
.welcome-list {
    max-width: 800px;
    margin: 40px auto;
    padding: 0;
    list-style: none;
    display: grid;
    gap: 16px;
}

.welcome-list li {
    background: #ffffff;
    border-radius: 14px;
    padding: 18px 22px 18px 50px;
    font-size: 21px;
    line-height: 1.5;
    color: #333;
    position: relative;
    box-shadow: 0 6px 18px rgba(0,0,0,0.06);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    display: flex;
    align-items: center;
}

.welcome-list li:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 24px rgba(0,0,0,0.1);
}

.welcome-list li::before {
    content: "✓";
    position: absolute;
    left: 18px;
    top: 18px;
    width: 22px;
    height: 22px;
    border-radius: 50%;
    background: #2ecc71;
    color: white;
    font-weight: bold;
    font-size: 13px;
    display: flex;
    align-items: center;
    justify-content: center;
}

@media (max-width: 600px) {

    .welcome-list {
        margin: 25px 15px;
        gap: 12px;
    }

    .welcome-list li {
        padding: 16px 16px 16px 44px;
        font-size: 15px;
    }

    .welcome-list li::before {
        left: 14px;
        top: 16px;
    }

}

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

<section class="welcome" aria-labelledby="welcome-title">
    <h1 style="text-align: center; max-width: 1200px; margin: 50px auto 0 auto;">
      <?= $home_title ?>
    </h1>


    <div class="form" style="margin: 0 auto; margin-top: 40px; margin-bottom: 80px">
      <form class="leadform rf-form js-rf-form" id="form" method="post" style="padding: 20px;" action="./integration/send.php">
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
