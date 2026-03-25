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
<html
  lang="<?= $site_lang ?>"
  data-wf-page="67c1ba3acfe5c27126bcc1f5"
  data-wf-site="67c1ba3acfe5c27126bcc191"
  class="w-mod-js wf-manrope-n4-active wf-manrope-n5-active wf-manrope-n6-active wf-active w-mod-ix">

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
  <link rel="icon" type="image/png" href="./favicon-96x96.png" sizes="96x96" />
  <link rel="icon" type="image/svg+xml" href="./favicon.svg" />
  <link rel="shortcut icon" href="./favicon.svg" />
  <link rel="apple-touch-icon" sizes="180x180" href="./apple-touch-icon.png" />
  <link rel="manifest" href="site.webmanifest" />
  <style>
    .wf-force-outline-none[tabindex="-1"]:focus {
      outline: none;
    }

    .navbar_link {
      font-size: 14px !important;
    } 
  </style>
  <link rel="stylesheet" href="./integration/default-integration.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/intl-tel-input@23.0.12/build/css/intlTelInput.css">

<title><?= $page_title_contact ?></title>
<meta property="og:type" content="website" />
<meta name="description" content="<?= $page_description_contact ?>">

  <meta content="summary_large_image" name="twitter:card" />
  <meta content="width=device-width, initial-scale=1" name="viewport" />
  <meta content="Webflow" name="generator" />
  <link href="normalize.css" rel="stylesheet" type="text/css" />
  <link href="webflow.css" rel="stylesheet" type="text/css" />
  <link
    href="papas-exceptional-site-198d4f.webflow.css"
    rel="stylesheet"
    type="text/css" />

  <style>
    @media (min-width: 992px) {
      html.w-mod-js:not(.w-mod-ix) [data-w-id="35ae0bc8-d895-deeb-51b5-eac5b8cf1794"] {
        opacity: 0;
        -webkit-transform: translate3d(0, 24px, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);
        -moz-transform: translate3d(0, 24px, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);
        -ms-transform: translate3d(0, 24px, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);
        transform: translate3d(0, 24px, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);
      }

      html.w-mod-js:not(.w-mod-ix) [data-w-id="30a34707-6eb3-a0bc-2b4d-b6131c4f1081"] {
        opacity: 0;
        -webkit-transform: translate3d(0, 24px, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);
        -moz-transform: translate3d(0, 24px, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);
        -ms-transform: translate3d(0, 24px, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);
        transform: translate3d(0, 24px, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);
      }

      html.w-mod-js:not(.w-mod-ix) [data-w-id="d48208f5-2047-ab4e-ef7b-f2de33c65ef3"] {
        -webkit-transform: translate3d(0, 24px, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);
        -moz-transform: translate3d(0, 24px, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);
        -ms-transform: translate3d(0, 24px, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);
        transform: translate3d(0, 24px, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);
        opacity: 0;
      }

      html.w-mod-js:not(.w-mod-ix) [data-w-id="ad008d0b-ca72-3722-c6cd-77686dc346c0"] {
        opacity: 0;
        -webkit-transform: translate3d(0, 24px, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);
        -moz-transform: translate3d(0, 24px, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);
        -ms-transform: translate3d(0, 24px, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);
        transform: translate3d(0, 24px, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);
      }

      html.w-mod-js:not(.w-mod-ix) [data-w-id="ad008d0b-ca72-3722-c6cd-77686dc346ca"] {
        opacity: 0;
        -webkit-transform: translate3d(0, 24px, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);
        -moz-transform: translate3d(0, 24px, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);
        -ms-transform: translate3d(0, 24px, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);
        transform: translate3d(0, 24px, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);
      }

      html.w-mod-js:not(.w-mod-ix) [data-w-id="2f80477f-23b3-153b-6ac3-96fff2ff8cc6"] {
        opacity: 0;
        -webkit-transform: translate3d(0, 24px, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);
        -moz-transform: translate3d(0, 24px, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);
        -ms-transform: translate3d(0, 24px, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);
        transform: translate3d(0, 24px, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);
      }

      html.w-mod-js:not(.w-mod-ix) [data-w-id="2f80477f-23b3-153b-6ac3-96fff2ff8cd0"] {
        opacity: 0;
        -webkit-transform: translate3d(0, 24px, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);
        -moz-transform: translate3d(0, 24px, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);
        -ms-transform: translate3d(0, 24px, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);
        transform: translate3d(0, 24px, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);
      }

      html.w-mod-js:not(.w-mod-ix) [data-w-id="e5af3ea2-e489-ee58-2953-21b064fb8231"] {
        opacity: 0;
        -webkit-transform: translate3d(0, 24px, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);
        -moz-transform: translate3d(0, 24px, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);
        -ms-transform: translate3d(0, 24px, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);
        transform: translate3d(0, 24px, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);
      }

      html.w-mod-js:not(.w-mod-ix) [data-w-id="7ba489e7-d1c8-85f9-e8bd-3ff3761719bd"] {
        opacity: 0;
        -webkit-transform: translate3d(0, 24px, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);
        -moz-transform: translate3d(0, 24px, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);
        -ms-transform: translate3d(0, 24px, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);
        transform: translate3d(0, 24px, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);
      }

      html.w-mod-js:not(.w-mod-ix) [data-w-id="80108313-5a20-1c62-1343-f315aeb7ef3f"] {
        opacity: 0;
        -webkit-transform: translate3d(0, 24px, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);
        -moz-transform: translate3d(0, 24px, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);
        -ms-transform: translate3d(0, 24px, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);
        transform: translate3d(0, 24px, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);
      }

      html.w-mod-js:not(.w-mod-ix) [data-w-id="5fbbd9d6-b291-c21e-e69e-3700890e19df"] {
        opacity: 0;
        -webkit-transform: translate3d(0, 24px, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);
        -moz-transform: translate3d(0, 24px, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);
        -ms-transform: translate3d(0, 24px, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);
        transform: translate3d(0, 24px, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);
      }

      html.w-mod-js:not(.w-mod-ix) [data-w-id="58b3e01c-d462-a6d1-a3e6-4b1761832b31"] {
        opacity: 0;
        -webkit-transform: translate3d(0, 24px, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);
        -moz-transform: translate3d(0, 24px, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);
        -ms-transform: translate3d(0, 24px, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);
        transform: translate3d(0, 24px, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);
      }

      html.w-mod-js:not(.w-mod-ix) [data-w-id="58b3e01c-d462-a6d1-a3e6-4b1761832b38"] {
        opacity: 0;
        -webkit-transform: translate3d(0, 24px, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);
        -moz-transform: translate3d(0, 24px, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);
        -ms-transform: translate3d(0, 24px, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);
        transform: translate3d(0, 24px, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);
      }

      html.w-mod-js:not(.w-mod-ix) [data-w-id="58b3e01c-d462-a6d1-a3e6-4b1761832b40"] {
        opacity: 0;
        -webkit-transform: translate3d(0, 24px, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);
        -moz-transform: translate3d(0, 24px, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);
        -ms-transform: translate3d(0, 24px, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);
        transform: translate3d(0, 24px, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);
      }

      html.w-mod-js:not(.w-mod-ix) [data-w-id="58b3e01c-d462-a6d1-a3e6-4b1761832b47"] {
        opacity: 0;
        -webkit-transform: translate3d(0, 24px, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);
        -moz-transform: translate3d(0, 24px, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);
        -ms-transform: translate3d(0, 24px, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);
        transform: translate3d(0, 24px, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);
      }

      html.w-mod-js:not(.w-mod-ix) [data-w-id="58b3e01c-d462-a6d1-a3e6-4b1761832b4f"] {
        opacity: 0;
        -webkit-transform: translate3d(0, 24px, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);
        -moz-transform: translate3d(0, 24px, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);
        -ms-transform: translate3d(0, 24px, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);
        transform: translate3d(0, 24px, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);
      }

      html.w-mod-js:not(.w-mod-ix) [data-w-id="58b3e01c-d462-a6d1-a3e6-4b1761832b61"] {
        opacity: 0;
        -webkit-transform: translate3d(0, 24px, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);
        -moz-transform: translate3d(0, 24px, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);
        -ms-transform: translate3d(0, 24px, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);
        transform: translate3d(0, 24px, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);
      }
    }
  </style>

  <script src="webfont.js" type="text/javascript"></script>
  <link rel="stylesheet" href="css.css" media="all" />
  <link href="favicon.png" rel="shortcut icon" type="image/x-icon" />
  <link href="css2.css" rel="stylesheet" />

  <style>
    /* Стилі для відміток на слайдерах */
    input[type="range"] {
      width: 100%;
      max-width: 800px;
      accent-color: #ffd700;
    }

    datalist {
      display: flex;
      justify-content: space-between;
      width: 100%;
      max-width: 800px;
      padding: 0;
    }

    datalist option {
      padding: 0;
      color: #ffd700;
      font-weight: bold;
    }

    /* Контейнер для слайдера та міток */
    .slider-container {
      position: relative;
      width: 100%;
      max-width: 800px;
      margin: 0 auto;
    }

    /* Стилі для міток */
    .slider-labels {
      position: relative;
      display: flex;
      justify-content: space-between;
      width: 100%;
    }

    .slider-label {
      color: #ffd700;
      font-size: 12px;
      transform: translateX(-50%);
    }

    a {
      text-decoration: none !important;
    }

    .iti__selected-dial-code,
    .iti__country-name {
      color: #000 !important;
    }

    
  </style>

</head>

<body cz-shortcut-listen="true">
  <div class="page-wrapper">
<header class="navbar_component w-nav" data-animation="default" data-collapse="medium" data-duration="400" data-easing="ease" data-easing2="ease" data-w-id="8e40c4b5-461f-531e-f642-15e88be2e74a" fs-scrolldisable-element="smart-nav" role="banner">
  <div class="navbar_container">
    <div class="navbar_logo-wrapper">
      <a href="<?= $site_url ?>">
        <img loading="lazy" src="favicon.svg" style="width: 25px; margin: 5px"/>
        <span style="color: black; font-weight: 700; font-size: 15px">
          <?= $source ?>
        </span>
      </a>
    </div>

    <nav class="navbar_menu is-page-height-tablet w-nav-menu" role="navigation">
      <div class="navbar_menu-links">
        <a class="navbar_link w-nav-link" href="<?= $site_url ?>#why-invest" style="background-color: transparent">
          <?= $text_why_invest ?>
        </a>
        <a class="navbar_link w-nav-link" href="<?= $site_url ?>#pricing" style="background-color: transparent">
          <?= $text_how_to_invest ?>
        </a>
        <a class="navbar_link w-nav-link" href="about.php" style="background-color: transparent">
          <?= $text_who_we_are ?>
        </a>
        <a class="navbar_link w-nav-link" href="<?= $site_url ?>#minimization" style="background-color: transparent">
          <?= $text_investment_risks ?>
        </a>
        <a class="navbar_link w-nav-link" href="<?= $site_url ?>#Beneficios" style="background-color: transparent">
          <?= $text_benefits ?>
        </a>
        <a class="navbar_link w-nav-link" href="<?= $site_url ?>#faq" style="background-color: transparent">
          <?= $text_faq ?>
        </a>
      </div>
    </nav>

    <div class="navbar_menu-buttons">
      <a class="button w-button" href="register.php" style="background-color: #ad92de;">
        <?= $text_log_in ?>
      </a>
      <a class="button w-button" href="register.php">
        <?= $text_sign_up ?>
      </a>
    </div>

    <div aria-controls="w-nav-overlay-0" aria-expanded="false" aria-haspopup="menu" aria-label="menu" class="navbar_menu-button w-nav-button" role="button" style="-webkit-user-select: text" tabindex="0">
      <div class="menu-icon1">
        <div class="menu-icon1_line-top"></div>
        <div class="menu-icon1_line-middle">
          <div class="menu-icon1_line-middle-inner"></div>
        </div>
        <div class="menu-icon1_line-bottom"></div>
      </div>
    </div>
  </div>
  <div class="w-nav-overlay" data-wf-ignore="" id="w-nav-overlay-0"></div>
</header>

    <main class="main-wrapper">

    </main>
  </div>

    </div>
  </div>

    </div>
  </div>



  <section class="">
    <div class="padding-global padding-section-medium">
      <div class="container-large">
        <div class="gradient-wrapper">
          <div
            data-w-id=""
            class="cta_component">
            <div class="cta_card">
              <div class="cta_card-content">
                <div class="max-width-large">
                  <div class="cta-content-wrapper">
<h1 class="heading-style-h1"><?= $contact_heading ?></h1>

<p class="text-size-regular" style="text-align: center;"><?= $contact_intro ?></p>

<h3 class="heading-style-h4" style="margin-top: 40px;"><?= $contact_how_to ?></h3>

<p class="text-size-regular" style="text-align: center;"><?= $contact_how_to_text ?></p>

<ul>
  <li><?= $contact_list_1 ?></li>
  <li><?= $contact_list_2 ?></li>
  <li><?= $contact_list_3 ?></li>
  <li><?= $contact_list_4 ?></li>
  <li><?= $contact_list_5 ?></li>
  <li><?= $contact_list_6 ?></li>
</ul>


<form action="./integration/send.php" class="leadform S’inscrire-form bottom form-reg c-form form1 rf-form js-rf-form" id="registrationForm" method="post" style="padding-bottom: 0px">
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

  <div class="block-center__wrapper">

    <div class="input-holder pos-r form-group input-wrap">
      <input class="form-control w-input" name="fname" placeholder="<?= $placeholder_fname ?>" required style="width: 100%;" type="text" value="">
    </div>

    <div class="input-holder pos-r form-group input-wrap">
      <input class="form-control w-input" name="lname" placeholder="<?= $placeholder_lname ?>" required style="width: 100%;" type="text" value="">
    </div>

    <div class="input-holder pos-r form-group input-wrap">
      <input class="form-control w-input" name="email" placeholder="<?= $placeholder_email ?>" required style="width: 100%;" type="email" value="">
    </div>

    <div class="input-holder pos-r form-group input-wrap">
      <input class="form-control w-input" name="fullphone" placeholder="" required style="width: 100%;" type="tel">
      <span class="error-msg hide"></span>
    </div>

    <div class="btn-holder js-buttons form-group input-wrap" style="display: flex; justify-content: center">
      <button class="submit btn_send" id="btn-payWithoutAuth" style="margin-bottom: 20px" type="submit">
        <?= $button_sign_up ?>
      </button>
    </div>
  </div>

  <div class="form-img">
    <img alt="visa" src="visa.png"/>
    <img alt="mastercard" src="mastercard.svg"/>
    <img alt="paypal" src="PayPal.svg.webp"/>
    <img alt="ssl security" src="sslsecure.svg"/>
  </div>

</form>

<p class="text-size-regular" style="text-align: center;"><?= $contact_send_message_text ?></p>

<h3 class="heading-style-h4" style="text-align: center; margin-bottom: 12px; margin-top: 30px;"><?= $contact_info ?></h3>


                    <p><?= $footer_contact_email ?></p>
                    <p><?= $footer_contact_address ?></p>
<p class="text-size-regular" style="text-align: center; margin-top: 30px;"><?= $contact_info_text ?></p>

                  </div>
                </div>
              </div>
              <img
                loading="lazy"
                src="pattern-background.svg"
                alt=""
                class="cta_background-image" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
  <style>
    /* Obщие стили для формы */
    input {
      box-sizing: border-box;
    }

    .spacer-small img {
      max-width: 700px;
      width: 100%;
      height: auto;
      display: block;
    }

    .S’inscrire-form {
      width: 500px;
      margin: 0 auto;
      padding: 20px;
      border-radius: 10px;
      font-family: Arial, sans-serif;

      background: radial-gradient(circle,
          rgba(255, 255, 255, 0.5) 0%,
          rgba(255, 255, 255, 0.5) 100%);
    }

    /* Стили для всех input полей */
    .S’inscrire-form input[type="text"],
    .S’inscrire-form input[type="tel"],
    .S’inscrire-form input[type="email"] {
      width: 100%;
      padding: 25px;
      margin-bottom: 15px;
      border: 1px solid black;
      border-radius: 15px;
      font-size: 16px;
      transition: border-color 0.3s ease;
      color: black;
    }

    /* Стили для фокуса на input полях */
    .S’inscrire-form input[type="text"]:focus,
    .S’inscrire-form input[type="tel"]:focus,
    .S’inscrire-form input[type="email"]:focus {
      border-color: #039e36;
      outline: none;
    }

    /* Кнопка отправки формы */
    .btn_send {
      background-color: #5217bf;
      border: none;
      padding: 15px;
      color: #fff;
      font-size: 18px;
      cursor: pointer;
      border-radius: 5px;
      width: 100%;
      transition: background-color 0.3s ease;
    }

    /* Эффект при наведении на кнопку */
    .btn_send:hover {
      background-color: #ff6347;
      /* Более светлый оттенок оранжевого */
    }

    /* Стили для заголовка или блока, если он будет добавлен */
    .block-center__wrapper {
      text-align: center;
      margin-bottom: 20px;
    }

    /* Стили для дополнительных элементов */
    .input-holder {
      position: relative;
    }

    .input-holder input {
      padding-left: 15px;
      /* Выравнивание текста внутри input */
    }

    .form-group {
      margin-bottom: 15px;
      /* Пространство между полями */
    }

    /* Убираем нижний padding формы */
    .form-reg {
      padding-bottom: 0;
      margin-top: 90px;
    }

    /* Стили для кнопок и их обертки */
    .js-buttons {
      margin-top: 20px;
    }
  </style>

<footer class="footer_component">
  <div class="padding-global">
    <div class="container-large">
      <div class="padding-vertical padding-xxlarge" style="padding-bottom: 2rem !important;">
        <div class="padding-bottom padding-xxlarge">
          <div class="w-layout-grid footer_top-wrapper">
            <div class="w-layout-grid footer_menu-wrapper" style="display: flex; flex-direction: column; align-items: flex-start;">
              <div class="footer_link-list" style="display: flex; flex-direction: column; gap: 10px">
                <div>
                  <a class="navbar_link w-nav-link footer-logo-link" href="#" style="background-color: transparent">
                    <img alt="" class="navbar1_logo" loading="lazy" src="favicon.svg" style="width: 50px; margin: 5px">
                    <span class="heading-style-h4" style="font-weight: 700; color: white;"><?= $footer_logo_name ?></span>
                  </a>
                </div>
                <div class="footer-list-wrapper">
                  <ul class="footer-list-first">
                    <li><a class="navbar_link" href="<?= $site_url ?>#why-invest" style="background-color: transparent"><span class="footer-link"><?= $footer_link_why_invest ?></span></a></li>
                    <li><a class="navbar_link" href="<?= $site_url ?>#pricing" style="background-color: transparent"><span class="footer-link"><?= $footer_link_how_to_invest ?></span></a></li>
                    <li><a class="navbar_link" href="<?= $site_url ?>#minimization" style="background-color: transparent"><span class="footer-link"><?= $footer_link_investment_risks ?></span></a></li>
                    <li><a class="navbar_link" href="<?= $site_url ?>#Beneficios" style="background-color: transparent"><span class="footer-link"><?= $footer_link_benefits ?></span></a></li>
                    <li><a class="navbar_link" href="<?= $site_url ?>#faq" style="background-color: transparent"><span class="footer-link"><?= $footer_link_faq ?></span></a></li>
                  </ul>
                  <ul class="footer-list-first">
                    <li><a class="navbar_link" href="about.php" style="background-color: transparent"><span class="footer-link"><?= $footer_link_who_we_are ?></span></a></li>
                    <li><a class="navbar_link" href="contact.php" style="background-color: transparent"><span class="footer-link"><?= $footer_link_contact ?></span></a></li>
                    <li><a class="navbar_link" href="private-policy.php" style="background-color: transparent"><span class="footer-link"><?= $footer_link_privacy_policy ?></span></a></li>
                    <li><a class="navbar_link" href="conditions.php" style="background-color: transparent"><span class="footer-link"><?= $footer_link_terms_conditions ?></span></a></li>
                    <li><a class="navbar_link" href="register.php" style="background-color: transparent"><span class="footer-link"><?= $footer_link_registration ?></span></a></li>
                  </ul>
                </div>
              </div>
            </div>
            <div class="footer_left-wrapper footer-flex">
              <div class="footer-list-right">
                <span class="heading-style-h4"><?= $footer_contact_title ?></span>
                <span class="footer-link"><?= $footer_contact_address ?></span>
                <span class="footer-link"><?= $footer_contact_email ?></span>
              </div>
            </div>
          </div>
          <p style="margin-top: 40px"><?= $footer_description ?></p>
          <p class="footer-copyright"><?= $footer_copyright ?></p>
        </div>
      </div>
    </div>
</footer>

  <noscript>
    <style>
        .leadform { display:none; }
    </style>
    <div>To submit the form, enable JavaScript</div>
  </noscript>


  <script
    src="jquery-3.5.1.min.dc5e7f18c8.js"
    type="text/javascript"></script>
  <script src="webflow.js" type="text/javascript"></script>

  <script src="jquery.min.js"></script>
  <div style="height: 0; overflow: hidden; position: absolute; width: 0">
    <a href="#">Pagina Principale</a>
    <a href="<?= $site_url ?>#why-invest">¿Por qué empezar a invertir?</a>
    <a href="<?= $site_url ?>#pricing">¿Cómo comenzar a invertir?    </a>
    <a href="about.php">¿Quién está detrás de <?= $source ?>?</a>
    <a href="<?= $site_url ?>#minimization">Riesgos asociados a la inversión</a>
    <a href="<?= $site_url ?>#Beneficios">Ventajas    </a>
    <a href="<?= $site_url ?>#faq">FAQ</a>
    <a href="contact.php">Contact</a>
    <a href="private-policy.php">Pravila privatnosti</a>
    <a href="conditions.php">Terms and conditions</a>
  </div>



  <script src="https://cdn.jsdelivr.net/npm/intl-tel-input@23.0.12/build/js/intlTelInput.min.js"></script>

  <!-- Keitaro -->
  <script src="./integration/validation.js"></script>
  


<!-- FAQ -->


  <script src="https://cdn.jsdelivr.net/npm/intl-tel-input@23.0.12/build/js/intlTelInput.min.js"></script>
  <script src="./integration/validation.js"></script>




<script>
document.addEventListener('DOMContentLoaded', () => {
  const jsonScript = document.getElementById('faq-json');
  if (!jsonScript) return;

  const data = JSON.parse(jsonScript.textContent);
  const faqList = document.getElementById('faq_list');

  data.mainEntity.forEach((item, index) => {
    const faqHTML = `
      <div class="faq_accordion">
        <div class="faq_question">
          <h3 class="text-size-large text-weight-semibold" style="font-weight: bold;">
            ${item.name}
          </h3>
          <div class="faq1_icon-wrapper">
            <img src="dropdown.svg" loading="lazy" alt="" class="icon-1x1-medium" />
          </div>
        </div>
        <div class="faq_answer">
          <p>${item.acceptedAnswer.text}</p>
          <div class="spacer-small"></div>
        </div>
      </div>
    `;

    faqList.insertAdjacentHTML('beforeend', faqHTML);
  });
});
</script>

<script>
document.addEventListener('click', function (e) {
  const question = e.target.closest('.faq_question');
  if (!question) return;

  const accordion = question.closest('.faq_accordion');

  document.querySelectorAll('.faq_accordion.active').forEach(item => {
    if (item !== accordion) item.classList.remove('active');
  });

  accordion.classList.toggle('active');
});
</script>
  <script src="script.js"></script>
</body>

</html>
