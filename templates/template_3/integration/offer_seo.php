<?php

// ========================================
// 1) ДАННЫЕ ОФФЕРА (НАСТРОЙКИ БАЙЕРА)
// ========================================
// ВНИМАНИЕ: Настройки для конкретного оффера
// МЕНЯТЬ: При настройке для нового оффера

// Основные параметры оффера
$source = "Venvion";                               // Название оффера
$form_country = 'de';                              // Страна по умолчанию
$form_language = 'de';                             // Язык по умолчанию
$form_phone_country = 'de';                      // Страна телефона (auto = автоопределение)
$form_is_autologin = false;                        // Автологин (true/false)
$form_only_countries = json_encode(['de']);        // Разрешенные страны



// ========================================
// 2) ДАННЫЕ ДЛЯ CRM (ЛИЧНЫЙ СЕТАП БАЙЕРА)
// ========================================
// ВНИМАНИЕ: Личные данные байера для API
// МЕНЯТЬ: При настройке для конкретного байера

$_SESSION['buyer_teamlead_chatid'] = '-1002909114943';    // ID чата тимлида
$_SESSION['buyer_affid'] = 'POL';                   // Аффилиат ID байера
$_SESSION['buyer_chatid'] = '234884403';                // ID чата байера
$_SESSION['buyer_token'] = 'xxqyswarblauwkt9ynrjntp7tp7qkvbq'; // API токен
$_SESSION['offer_id'] = 'OFFER_ID';                         // ID оффера в системе
$_SESSION['affiliate_id'] = 'AFFILIATE_ID';              // ID аффилиата в системе

// ========================================
// 3) ТЕХНИЧЕСКИЕ НАСТРОЙКИ (НЕ ТРОГАТЬ)
// ========================================
// ВНИМАНИЕ: Техническая конфигурация системы
// НЕ МЕНЯТЬ: Байеру не изменять!


// Домен для отслеживания
$domain = $_SERVER['HTTP_HOST'];

// Сохранение настроек оффера в сессию
$_SESSION['form_is_autologin'] = $form_is_autologin;
$_SESSION['source'] = $source;
$_SESSION['form_domain'] = $domain;

// Безопасность сессии
if (!isset($_SESSION['security_token'])) {
    $_SESSION['security_token'] = 'SECURE_SESSION_AUTHENTICATION_TOKEN';
}

?>
