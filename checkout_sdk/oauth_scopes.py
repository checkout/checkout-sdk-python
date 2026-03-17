from __future__ import absolute_import

from enum import Enum


class OAuthScopes(str, Enum):
    VAULT = 'vault'
    VAULT_INSTRUMENTS = 'vault:instruments'
    VAULT_TOKENIZATION = 'vault:tokenization'
    VAULT_CUSTOMERS = 'vault:customers'
    VAULT_REAL_TIME_ACCOUNT_UPDATER = 'vault:real-time-account-updater'
    VAULT_APME_ENROLLMENT = 'vault:apme-enrollment'
    VAULT_CARD_METADATA = 'vault:card-metadata'
    VAULT_NETWORK_TOKENS = 'vault:network-tokens'
    
    GATEWAY = 'gateway'
    GATEWAY_PAYMENT = 'gateway:payment'
    GATEWAY_PAYMENT_DETAILS = 'gateway:payment-details'
    GATEWAY_PAYMENT_AUTHORIZATION = 'gateway:payment-authorizations'
    GATEWAY_PAYMENT_VOIDS = 'gateway:payment-voids'
    GATEWAY_PAYMENT_CAPTURES = 'gateway:payment-captures'
    GATEWAY_PAYMENT_REFUNDS = 'gateway:payment-refunds'
    GATEWAY_PAYMENT_CANCELLATIONS = 'gateway:payment-cancellations'
    GATEWAY_PAYMENT_CONTEXTS = 'gateway:payment-contexts'
    
    FX = 'fx'
    PAYOUTS_BANK_DETAILS = 'payouts:bank-details'
    SESSIONS_APP = 'sessions:app'
    SESSIONS_BROWSER = 'sessions:browser'
    
    DISPUTES = 'disputes'
    DISPUTES_VIEW = 'disputes:view'
    DISPUTES_PROVIDE_EVIDENCE = 'disputes:provide-evidence'
    DISPUTES_ACCEPT = 'disputes:accept'
    DISPUTES_SCHEME_FILES = 'disputes:scheme-files'
    
    MARKETPLACE = 'marketplace'
    ACCOUNTS = 'accounts'
    
    TRANSFERS = 'transfers'
    TRANSFERS_CREATE = 'transfers:create'
    TRANSFERS_VIEW = 'transfers:view'
    
    FLOW = 'flow'
    FLOW_WORKFLOWS = 'flow:workflows'
    FLOW_EVENTS = 'flow:events'
    FLOW_REFLOW = 'flow:reflow'
    
    FILES = 'files'
    FILES_RETRIEVE = 'files:retrieve'
    FILES_UPLOAD = 'files:upload'
    FILES_DOWNLOAD = 'files:download'
    
    BALANCES = 'balances'
    BALANCES_VIEW = 'balances:view'
    
    MIDDLEWARE = 'middleware'
    MIDDLEWARE_MERCHANTS_SECRET = 'middleware:merchants-secret'
    MIDDLEWARE_MERCHANTS_PUBLIC = 'middleware:merchants-public'
    
    REPORTS = 'reports'
    REPORTS_VIEW = 'reports:view'
    
    FINANCIAL_ACTIONS = 'financial-actions'
    FINANCIAL_ACTIONS_VIEW = 'financial-actions:view'
    
    CARD_MANAGEMENT = 'card-management'
    
    ISSUING_CARD_MGMT = 'issuing:card-mgmt'
    ISSUING_CARD_MANAGEMENT_READ = 'issuing:card-management-read'
    ISSUING_CARD_MANAGEMENT_WRITE = 'issuing:card-management-write'
    ISSUING_CLIENT = 'issuing:client'
    ISSUING_CONTROLS_READ = 'issuing:controls-read'
    ISSUING_CONTROLS_WRITE = 'issuing:controls-write'
    ISSUING_TRANSACTIONS_READ = 'issuing:transactions-read'
    ISSUING_TRANSACTIONS_WRITE = 'issuing:transactions-write'
    ISSUING_DISPUTES = 'issuing-disputes'
    ISSUING_DISPUTES_READ = 'issuing:disputes-read'
    ISSUING_DISPUTES_WRITE = 'issuing:disputes-write'
    
    TRANSACTIONS = 'transactions'
    
    IDENTITY_VERIFICATION = 'identity-verification'

    PAYMENT_CONTEXT = 'Payment Context'

    FORWARD = 'forward'
    FORWARD_SECRETS = 'forward:secrets'
    
    PAYMENT_SESSIONS = 'payment-sessions'
    PAYMENTS_SEARCH = 'payments:search'
