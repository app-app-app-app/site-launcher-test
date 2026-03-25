<?php

/**
 * Function for logging to integration_errors.php
 */
function logError($message)
{
  // Use protected log file with .php extension (works with Nginx)
  $logFile = __DIR__ . '/integration_errors.php';

    // Set correct timezone (UTC+3 for Ukraine)
    date_default_timezone_set('Europe/Kiev');
    $timestamp = date('Y-m-d H:i:s');

    $logMessage = "[$timestamp] $message" . PHP_EOL;

    // Add new logs at the end of file (better performance)
    $result = file_put_contents($logFile, $logMessage, FILE_APPEND | LOCK_EX);
}

/**
 * Log timing statistics for API calls
 *
 * @param string $service The service name (Telegram, Keitaro, etc.)
 * @param mixed $ch The cURL handle
 */
function logTimingStats($service, $ch, $identifier = null)
{
    $userIdentifier = getPost('click_id');
    $connectTime = curl_getinfo($ch, CURLINFO_CONNECT_TIME);
    $totalTime = curl_getinfo($ch, CURLINFO_TOTAL_TIME);
    
    $connectTimeMs = round($connectTime * 1000, 2);
    $totalTimeMs = round($totalTime * 1000, 2);
    
    $logMessage = "$service Stats | User: $userIdentifier | Connect: {$connectTimeMs}ms | Total: {$totalTimeMs}ms";
    
    if ($identifier) {
        $logMessage .= " | ID: $identifier";
    }
    
    logError($logMessage);
}

/**
 * Looks at IP's from X-Fowarded-For and REMOTE_ADDR and returns the first
 *
 * @return string
 */
function getIP()
{
    if (!empty($_SERVER['HTTP_CLIENT_IP'])) {
        $ip = $_SERVER['HTTP_CLIENT_IP'];
    } elseif (!empty($_SERVER['HTTP_X_FORWARDED_FOR'])) {
        $ips = explode(',', $_SERVER['HTTP_X_FORWARDED_FOR']);
        $ip = trim($ips[0]);
    } else {
        $ip = $_SERVER['REMOTE_ADDR'];
    }

    return $ip;
}

/**
 * Generate a random password of a given length
 *
 * @param int $length // The desired length of the generated password
 *
 * @return string // The generated password
 */
function generatePassword($length = 12)
{
    $characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
    $charactersLength = strlen($characters);
    $randomPassword = '';

    for ($i = 0; $i < $length; $i++) {
        $randomIndex = rand(0, $charactersLength - 1);
        $randomPassword .= $characters[$randomIndex];
    }

    return $randomPassword;
}

/**
 * Returns the value from the $_POST array, or the default value
 * if the key is not set
 *
 * @param string $key     The key to look for in the $_POST array
 * @param mixed  $default The default value to return if the key is not set
 *
 * @return mixed
 */
function getPost($key, $default = null)
{
    if (isset($_POST[$key])) {
        return $_POST[$key];
    }
    return $default;
}

/**
 * Send a message to a specified Telegram chat.
 *
 * This function uses the Telegram Bot API to send a message to a chat identified by the provided chat ID.
 * It handles the request via cURL and logs any errors encountered during the process.
 *
 * @param string $messageText The message content to be sent to the chat.
 * @param string $chatid The unique identifier for the target chat where the message will be sent.
 */
function sendTGMessage($messageText, $chatid)
{
    $messageData = array(
        'chat_id' => $chatid,
        'text' => $messageText,
    );

    $ch = curl_init(TGBOT_ENDPOINT);
    curl_setopt($ch, CURLOPT_POST, 1);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $messageData);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

    $response = curl_exec($ch);
    $error = curl_error($ch);
    
    logTimingStats('Telegram', $ch, $chatid);
    curl_close($ch);

    if ($error) {
        logError("Telegram Error: $error | Message: $messageText | ChatID: $chatid");
    }
}

/**
 * Send a message to the buyer's chat and their team lead's chat if available.
 *
 * @param string $messageText The message to be sent to the chats.
 * @param array $buyerData The buyer data array with chatid and buyer_teamlead_chatid.
 */
function sendTGMessageToBuyers($messageText, $buyerData)
{
    $chatIds = [];
    $buyerChatId = $buyerData['buyer_chat_id'] ?? '';
    $buyerTeamleadChatId = $buyerData['buyer_teamlead_chatid'] ?? '';

    // Add buyer's chat ID if available
    if (!empty($buyerChatId)) {
        $chatIds[] = $buyerChatId;
    }
     // Add buyer's TeamLead chat ID if available
     if (!empty($buyerTeamleadChatId)) {
        $chatIds[] = $buyerTeamleadChatId;
    }

    // Note: buyer_teamlead_chatid logic simplified since we no longer have BuyersList
    // If buyer_teamlead_chatid chat ID is needed, it should be passed separately
    
    $chatIds = array_filter(array_unique($chatIds));

    foreach ($chatIds as $chatId) {
        sendTGMessage($messageText, $chatId);
    }
}



/**
 * Check if the submitted data contains test keywords
 * 
 * @param array $data The data array to check
 * @return bool Returns true if test keywords are found, false otherwise
 */
function isTestData($data)
{
    $testKeywords = ['test'];
    $fieldsToCheck = ['first_name', 'last_name'];

    foreach ($fieldsToCheck as $field) {
        if (isset($data[$field])) {
            $value = strtolower(trim($data[$field]));

            foreach ($testKeywords as $keyword) {
                if (strpos($value, $keyword) !== false) {
                    return true;
                }
            }
        }
    }

    return false;
}



/**
 * Block spam request by logging attempt and returning fake success
 * 
 * @param array $buyerData Optional buyer data for Telegram notifications
 */
function blockSpamRequest($buyerData = [])
{
    $spam_data = 
        "🔒 SECURITY ALERT: SPAM_ATTEMPT_BLOCKED\n\n" .
        "📅 TIMESTAMP: " . date('Y-m-d H:i:s') . "\n\n" .
        "🌐 REQUEST INFO:\n" .
        "IP: " . ($_SERVER['REMOTE_ADDR'] ?? 'unknown') . "\n" .
        "User Agent: " . ($_SERVER['HTTP_USER_AGENT'] ?? 'unknown') . "\n" .
        "Session Token: " . ($_SESSION['security_token'] ?? 'MISSING') . "\n" .
        "JS Token: " . ($_POST['js_token'] ?? 'MISSING') . "\n\n" .
        "👤 LEAD INFO:\n" .
        "fname: " . getPost('fname') . "\n" .
        "lname: " . getPost('lname') . "\n" .
        "email: " . getPost('email') . "\n" .
        "fullphone: " . getPost('fullphone') . "\n" .
        "source: " . getPost('source') . "\n" .
        "country: " . getPost('country') . "\n" .
        "language: " . getPost('language') . "\n" .
        "domain: " . getPost('domain') . "\n\n" .
        "📊 TRACKING DATA:\n" .
        "Keitaro Click ID: " . getPost('click_id') . "\n" .
        "UTM Campaign: " . getPost('utm_campaign') . "\n" .
        "UTM Source: " . getPost('utm_source');

    
    $spamLeadMessage = 
        "🚨 BLOCKED SPAM ATTEMPT 🚨\n\n" .
        "First Name: " . getPost('fname') . "\n" .
        "Last Name: " . getPost('lname') . "\n" .
        "Email: " . getPost('email') . "\n" .
        "Phone: " . getPost('fullphone') . "\n" .
        "Offer Name: " . getPost('source') . "\n" .
        "Country: " . getPost('country') . "\n" .
        "Language: " . getPost('language') . "\n" .
        "Domain: " . getPost('domain') . "\n" .
        "Keitaro Click ID: " . getPost('click_id') . "\n" .
        "Status: ⛔ BLOCKED (SPAM)\n";
    
    logError("SPAM ATTEMPT: " . $spam_data);
    
    if (isTestData($_POST)) {
        sendTGMessage($spam_data, TGBOT_TECH_TEST_CHATID);
    }
    
    sendTGMessage($spam_data, TGBOT_TECHLOG_CHATID);
    if (!empty($buyerData)) {
        sendTGMessageToBuyers($spamLeadMessage, $buyerData);
    }
    
    header('Content-Type: application/json');
    echo json_encode(['success' => true, 'message' => 'Registration successful']);
    exit;
}








