<?php
session_start();
require_once 'offer_seo.php';

?>

<!DOCTYPE html>
<html>

<head>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
  <title>Template</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/intl-tel-input@23.0.12/build/css/intlTelInput.css">

  <!-- form style -->
  <style>
    * {
      box-sizing: border-box;
    }

    .registration-form {
      max-width: 450px;
      margin: 30px auto;
      border-radius: 10px;
      overflow: hidden;
      box-shadow: rgba(149, 157, 165, 0.2) 0px 8px 24px;
    }

    .registration-form__body {}

    .registration-form__title {
      font-size: 28px;
      font-weight: 600;
      background-color: #eb0000;
      color: #fff;
      text-align: center;
      padding: 10px;
      margin: 0;
    }

    .registration-form__inner {
      padding: 10px;
    }

    .registration-form__wrapper {
      margin: 0;
    }

    .registration-form__inputs {}

    .inputs-form {
      display: flex;
      flex-direction: column;
      row-gap: 10px;
      padding: 10px 0;
    }

    .inputs-form__input {
      width: 100%;

    }

    .inputs-form__input input {
      width: 100%;
      outline: 0;
      height: 40px;
      padding: 0 15px;
      transition: .3s all;
      border: 2px solid #e2e5e7;
      border-radius: 5px;
    }

    .inputs-form__input input:focus {
      box-shadow: rgba(0, 0, 0, 0.24) 0px 3px 8px;
    }

    .inputs-form__actions {}

    .inputs-form__btn {
      width: 100%;
      padding: 10px 20px;
      font-weight: 600;
      font-size: 28px;
      border-radius: 5px;
      box-shadow: rgba(99, 99, 99, 0.2) 0px 2px 8px 0px;
      background-color: #eb0000;
      border: 2px solid #fff;
      color: #fff;
      text-transform: uppercase;
      transition: .5s all;
    }

    .inputs-form__btn:hover {
      background-color: transparent;
      border-color: #eb0000;
      color: #000;
      letter-spacing: 2px;
    }

    .inputs-form__btn:active {
      transform: scale(0.95);
      letter-spacing: 0;
    }

    a {
      cursor: pointer;
    }
  </style>
  <!-- end form style -->

  <!-- default form style -->
  <style>
    .iti.iti--allow-dropdown {
      width: 100%;
    }

    .leadform {
      position: relative;
    }

    .form-preloader {
      position: absolute;
      top: 0;
      bottom: 0;
      right: 0;
      left: 0;
      background: #fff;
      z-index: 4;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .error-msg {
      padding-bottom: 10px;
      color: red;
      font-size: 14px;
      text-align: right;
    }

    .spinner {
      animation: rotate 2s linear infinite;
      z-index: 2;
      position: absolute;
      top: 50%;
      left: 50%;
      margin: -25px 0 0 -25px;
      width: 50px;
      height: 50px;
    }

    .spinner .path {
      stroke: #0077db;
      stroke-linecap: round;
      animation: dash 1.5s ease-in-out infinite;
    }

    .hide,
    .hidden {
      display: none !important;
    }

    @keyframes rotate {
      100% {
        transform: rotate(360deg);
      }
    }

    @keyframes dash {
      0% {
        stroke-dasharray: 1, 150;
        stroke-dashoffset: 0;
      }

      50% {
        stroke-dasharray: 90, 150;
        stroke-dashoffset: -35;
      }

      100% {
        stroke-dasharray: 90, 150;
        stroke-dashoffset: -124;
      }
    }
  </style>
  <!-- end default form style -->


</head>

<body>
  <section class="registration-form">
    <div class="registration-form__body">
      <h2 class="registration-form__title" data-i18n="">Change your life today</h2>
      <div class="registration-form__inner">
         class="leadform" action="send.php" method="POST">
          <div class="registration-form__inputs inputs-form">
            <input type="hidden" name="js_token" value="<?= $jsToken; ?>">

            <div style="position:absolute; left:-9999px; opacity:0; height:0; overflow:hidden;">
              <input type="text" name="website" tabindex="-1" autocomplete="off">
              <input type="text" name="company" style="position:absolute; left:-9999px;">
            </div>

            <input type="hidden" name="country" value="<?php echo $form_country; ?>">
            <input type="hidden" name="language" value="<?php echo $form_language; ?>">
            <input type="hidden" name="phone_country" value="<?php echo $form_phone_country; ?>">
            <input type="hidden" name="only_countries" value='<?php echo $form_only_countries; ?>'>

            <div class="form-preloader hidden">
              <svg width="50" height="50" class="spinner" viewBox="0 0 50 50">
                <circle class="path" cx="25" cy="25" r="20" fill="none" stroke-width="5">
                </circle>
              </svg>
            </div>

            <div class="inputs-form__input">
              <input type="text" name="fname" placeholder="Name" required="required">
            </div>
            <div class="inputs-form__input">
              <input type="text" name="lname" placeholder="Last Name" required="required">
            </div>
            <div class="inputs-form__input">
              <input type="email" name="email" placeholder="Email" required="required">
            </div>
            <div class="inputs-form__input">
              <input type="tel" name="fullphone" required="required">
              <div class="error-msg hide"></div>
            </div>
          </div>
          <div class="inputs-form__actions">
            <button class="inputs-form__btn" type="submit">Registration</button>
          </div>
        </form>

      </div>
    </div>
  </section>

  <noscript>
    <style>
        .leadform { display:none; }
    </style>
    <div>To submit the form, enable JavaScript</div>
  </noscript>
  <script src="https://cdn.jsdelivr.net/npm/intl-tel-input@23.0.12/build/js/intlTelInput.min.js"></script>
  <script src="./validation.js"></script>
  <script>
  </script>
</body>

</html>