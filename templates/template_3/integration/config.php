<?php

// TelegramBot values
define('TGBOT_TOKEN', '8176792283:AAH_6c6CAcMuQyM-yS6G8MiJ0C1nh1aLjeg');
define('TGBOT_TECHLOG_CHATID', '-1003013176906');   // AM Domains Log
define('TGBOT_TECH_TEST_CHATID', '-1003164975874'); // AM Domains Test Log

define('TGBOT_ENDPOINT', 'https://api.telegram.org/bot' . TGBOT_TOKEN . '/sendMessage');

// Lead Distribution API v.2 endpoint
define('ELNOPY_ENDPOINT', 'https://yourleads.org/api/affiliates/v2/leads');


// Session security
define('SECURE_SESSION_TOKEN', 'SECURE_SESSION_AUTHENTICATION_TOKEN');

/**
 * Get buyer data from session
 * 
 * This function retrieves buyer data from session variables that were 
 * set in offer_fb.php from Raw Click subid parameters.
 * 
 * @return array Buyer data array with token, chatid, buyer_teamlead_chatid
 */
function getBuyerDataFromSession()
{
    return [
        'token' => $_SESSION['buyer_token'] ?? '',
        'buyer_chat_id' => $_SESSION['buyer_chatid'] ?? '',
        'buyer_teamlead_chatid' => $_SESSION['buyer_teamlead_chatid'] ?? ''
    ];
}

/**
 * Prepare data for Lead Distribution API v.2
 * 
 * This function filters and prepares only the fields required by the 
 * Lead Distribution API v.2 specification.
 * 
 * @param array $data The full data array from getData()
 * @return array Filtered data array for API
 */
function prepareApiData($data)
{
    $apiData = [
        // Required field
        'ip' => $data['ip'],
        
        // Optional fields
        'country_code' => $data['country_code'] ?? null,
        'lead_language' => $data['lead_language'] ?? null,
        'is_test' => $data['is_test'],
        
        // Lead Profile fields
        'email' => $data['email'],
        'first_name' => $data['first_name'],
        'last_name' => $data['last_name'],
        'password' => $data['password'],
        'phone' => $data['phone'],
        'affiliate_id' => $data['affiliate_id'] ?? null,
        'offer_id' => $data['offer_id'] ?? null,
        
        'aff_sub'  => $data['fbclid'],
        'aff_sub2'  => $data['source'],
        'aff_sub3'  => $data['click_id'],
        'aff_sub4'  => $data['pfb'],
        'aff_sub5'  => $data['utm_term'],
        'aff_sub6'  => $data['utm_campaign'],
        'aff_sub7'  => $data['utm_source'],
        'aff_sub8' => $data['utm_placement'],
        'aff_sub9' => $data['adset_name'],
        'aff_sub10' => $data['ad_id'],
		'aff_sub11' => $data['domain'],
        
       

        
    ];
    
    // Remove null/empty values
    return array_filter($apiData, function($value) {
        return $value !== null && $value !== '';
    });
}

