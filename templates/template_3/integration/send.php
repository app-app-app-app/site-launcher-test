<?php
session_start();
require_once 'config.php';
require_once 'helpers.php';

$phone = preg_replace('/[^0-9+]/', '', getPost('fullphone'));
$country = strtolower(getPost('country'));

$countryPrefixes = [
    'en' => '+1',
    'de' => '+49',
    'ru' => '+7',
    'it' => '+39',
    'tr' => '+90',
    'pt' => '+351',
    'pl' => '+48',
    'hu' => '+36',
    'ro' => '+40',
    'ae' => '+971',
    'jp' => '+81',
    'br' => '+55',
    'ca' => '+1',
    'sg' => '+65',
    'hk' => '+852',
    'in' => '+91',
    'mx' => '+52',
    'pe' => '+51',
    'cl' => '+56',
    'gb' => '+44',
    'cs' => '+420',
    'el' => '+30',
    'hr' => '+385',
    'lv' => '+371',
    'no' => '+47',
    'fr' => '+33',
    'es' => '+34',
    'ch' => '+41',
    'us' => '+1',
    'ua' => '+380',
    'kz' => '+7',
    'uz' => '+998',
    'ge' => '+995',
    'am' => '+374',
    'az' => '+994',
    'by' => '+375',
    'lt' => '+370',
    'ee' => '+372',
    'dk' => '+45',
    'se' => '+46',
    'fi' => '+358',
    'nl' => '+31',
    'be' => '+32',
    'at' => '+43',
    'ie' => '+353',
    'is' => '+354',
    'gr' => '+30',
    'cn' => '+86',
    'kr' => '+82',
    'th' => '+66',
    'vn' => '+84',
    'id' => '+62',
    'my' => '+60',
    'ph' => '+63',
    'pk' => '+92',
    'bd' => '+880',
    'lk' => '+94',
    'sa' => '+966',
    'qa' => '+974',
    'kw' => '+965',
    'om' => '+968',
    'bh' => '+973',
    'il' => '+972',
    'za' => '+27',
    'eg' => '+20',
    'ma' => '+212',
    'ng' => '+234',
    'ke' => '+254',
    'gh' => '+233',
    'tn' => '+216',
    'ar' => '+54',
    'co' => '+57',
    've' => '+58',
    'uy' => '+598',
    'py' => '+595',
    'bo' => '+591',
    'cr' => '+506',
    'pa' => '+507',
    'do' => '+1',
    'gt' => '+502',
];

if (isset($countryPrefixes[$country])) {

    if (strpos($phone, $countryPrefixes[$country]) !== 0) {
        http_response_code(403);
        exit('Phone country mismatch');
    }
}


$host = isset($_SESSION['form_domain']) ? 'https://' . $_SESSION['form_domain'] : '';

header("Access-Control-Allow-Origin: $host");



// Get buyer data from session
$CURRENT_BUYER = getBuyerDataFromSession();




$js_token = $_POST['js_token'];
$session_token = $_SESSION['security_token'] ?? '';

// if (empty($js_token) || $session_token !== SECURE_SESSION_TOKEN) {
//     blockSpamRequest($CURRENT_BUYER);
// } else {
//     $_SESSION['security_token'] = 'SUCCESS';
// }

/**
 * Returns the lead registration payload for CRM
 *
 * @param array $buyerData The buyer data array
 * @return array $data The data to use to build the payload
 */
function getData($buyerData)
{
    return [
        // User data (from form)
        'first_name' => getPost('fname'),
        'last_name' => getPost('lname'),
        'email' => getPost('email'),
        'phone' => getPost('fullphone'),
        'source' => $_SESSION['source'] ?? '',
        'pfb' => 'SEO',
        
        // System generated data
        'password' => generatePassword(),
        'ip' => getIP(),
        // 'ip' => '190.115.24.9',
    
        'is_test' => isTestData($_POST),
        
        // Location and language data
        'country_code' => getPost('country'),
        'lead_language' => getPost('language'),
        
        // Affiliate and offer data
        'affiliate_id' => $_SESSION['affiliate_id'] ?? '',
        'offer_id' => $_SESSION['offer_id'] ?? '',
        'buyer_affid' => $_SESSION['buyer_affid'] ?? '',
        
        // UTM and tracking data
        'domain' => $_SESSION['form_domain'],
        
        'utm_campaign' => 'SEO',
        'utm_medium' => 'SEO',
        'utm_term' => 'SEO',
        'fbclid'   => 'SEO',
        'utm_source' => 'SEO',
        'utm_placement' => 'SEO',
        'adset_name'    => 'SEO',
        'ad_id'         => 'SEO',
        

        'click_id' => 'SEO',
        
        // Form configuration
        'is_autologin' => $_SESSION['form_is_autologin'],
        'js_token' => getPost('js_token'),
        
    ];
}

if ($_SERVER["REQUEST_METHOD"] == "POST") {

    if (isset($_POST['fname']) && isset($_POST['email']) && isset($_POST['fullphone'])) {

        // Authorization
        $redirect_url = '';

        // Request to Lead Distribution API 
        $data = getData($CURRENT_BUYER);
        $apiData = prepareApiData($data);
        
        $curl_crm = curl_init();
        curl_setopt_array(
            $curl_crm,
            array(
                CURLOPT_URL => ELNOPY_ENDPOINT,
                CURLOPT_RETURNTRANSFER => true,
                CURLOPT_ENCODING => '',
                CURLOPT_MAXREDIRS => 10,
                CURLOPT_CONNECTTIMEOUT => 10,
                CURLOPT_TIMEOUT => 20,
                CURLOPT_FOLLOWLOCATION => true,
                CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
                CURLOPT_CUSTOMREQUEST => 'POST',
                CURLOPT_POSTFIELDS => json_encode($apiData),
                CURLOPT_HTTPHEADER => array(
                    'Content-Type: application/json',
                    'Authorization: ' . $CURRENT_BUYER['token'],
                    'Accept: application/json',
                ),
            )
        );
        $response_crm = curl_exec($curl_crm);
        $error = curl_error($curl_crm);
        
        logTimingStats('CRM', $curl_crm);
        $status = curl_getinfo($curl_crm, CURLINFO_HTTP_CODE);
        curl_close($curl_crm);

        $data['crm_response_status'] = $status;
        $decoded_response_crm = json_decode($response_crm, true);
        $data['crm_response'] = $decoded_response_crm;

        $BuyerTelegramMessage =
            "🎉New Lead\n\n" .
            "Email: " . $data['email'] . "\n" .
            "Buyer: " . $data['buyer_affid'] . "\n" .
            "Country: " . $data['country_code'] . "\n" .
            "Language: " . $data['lead_language'] . "\n" .
            "Domain: " . $data['domain'] . "\n" .
            "Source: " . $data['source'] . "\n" .
            "UTM Campaign: " . $data['utm_campaign'] . "\n" .
            "UTM Medium: " . $data['utm_medium'] . "\n" .
            "UTM Term: " . $data['utm_term'] . "\n" .
            "Keitaro Click ID: " . $data['click_id'] . "\n" .
            "Lead in CRM: " . ($status === 200 ? "Yes" : "No") . "\n";

        if ($status === 200 && isset($data['crm_response']['lead_uuid'])) {
            $BuyerTelegramMessage .= "Lead UUID: " . $data['crm_response']['lead_uuid'] . "\n";
        } else {
            $BuyerTelegramMessage .= "Error: " . $data['crm_response_status'] . "\n";
            if (isset($data['crm_response']['message'])) {
                $BuyerTelegramMessage .= "Message: " . $data['crm_response']['message'] . "\n";
            }
        }

        // Response handler
        if ($status === 200 && isset($data['crm_response']['lead_uuid'])) {

            if ($data['is_autologin'] && isset($data['crm_response']) && isset($data['crm_response']['auto_login_url'])) {
                $redirect_url = $data['crm_response']['auto_login_url'];
                $data['success_autologin'] = true;
            } else {
                $data['success_autologin'] = false;
            }

            try {
                if (isTestData($data)) {
                    sendTGMessage(json_encode($data, JSON_PRETTY_PRINT), TGBOT_TECH_TEST_CHATID);
                }
                sendTGMessage(json_encode($data, JSON_PRETTY_PRINT), TGBOT_TECHLOG_CHATID);
                sendTGMessageToBuyers($BuyerTelegramMessage, $CURRENT_BUYER);
            } catch (Exception $e) {
                logError("Error while sending a telegram log: " . $e->getMessage());
            }

            echo json_encode([
                'success' => true,
                'pfb' => 'SEO',
                'click_id' => 'SEO',
                'lead_language' => getPost('language'),
                'redirect_url' => $redirect_url,
            ]);

            exit;
        } else {
            try {
                if (isTestData($data)) {
                    sendTGMessage(json_encode($data, JSON_PRETTY_PRINT), TGBOT_TECH_TEST_CHATID);
                }
                sendTGMessage(json_encode($data, JSON_PRETTY_PRINT), TGBOT_TECHLOG_CHATID);
                sendTGMessageToBuyers($BuyerTelegramMessage, $CURRENT_BUYER);
            } catch (Exception $e) {
                logError("Error while sending a telegram log: " . $e->getMessage());
            }

            echo json_encode([
                'success' => false,
                'lead_language' => getPost('language'),
                'click_id' => 'SEO',
                'redirect_url' => $redirect_url,
            ]);

            exit;
        }
    } else {
        logError("Error: Not all required fields have been submitted. Domain " . getPost('domain') . " IP: " . getIP());
        sendTGMessage("Error: Not all required fields have been submitted. Domain " . getPost('domain') . " IP: " . getIP(), TGBOT_TECHLOG_CHATID);
    }
} else {
    logError("Error: POST request was pending. Domain " . getPost('domain') . " IP: " . getIP());
    sendTGMessage("Error: POST request was pending. Domain " . getPost('domain') . " IP: " . getIP(), TGBOT_TECHLOG_CHATID);
}
