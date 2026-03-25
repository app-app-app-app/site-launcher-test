<?php

// ========================================
// 1) ДАННЫЕ ОФФЕРА (НАСТРОЙКИ БАЙЕРА)
// ========================================
// ВНИМАНИЕ: Настройки для конкретного оффера
// МЕНЯТЬ: При настройке для нового оффера

// Основные параметры оффера
$source = "Italoxflow";                      // Название оффера
$form_country = 'it';                              // Страна по умолчанию
$form_language = 'it';                             // Язык по умолчанию
$form_phone_country = 'it';                      // Страна телефона (auto = автоопределение)
$form_is_autologin = false;                        // Автологин (true/false)
$form_only_countries = json_encode(['it']);       // Разрешенные страны


// ========================================
// 2) ДАННЫЕ ДЛЯ CRM (ЛИЧНЫЙ СЕТАП БАЙЕРА)
// ========================================
// ВНИМАНИЕ: Личные данные байера для API
// МЕНЯТЬ: При настройке для конкретного байера

$_SESSION['buyer_teamlead_chatid'] = '-1003243124891';    // ID чата тимлида
$_SESSION['buyer_affid'] = 'TNA';                   // Аффилиат ID байера
$_SESSION['buyer_chatid'] = '5935076163';                // ID чата байера
$_SESSION['buyer_token'] = '86dbmrlhbhjv8cjkx771h97cr7kaydpfg'; // API токен
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
