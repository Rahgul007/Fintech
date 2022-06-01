CREATE TABLE `MASTER_DATA` (
  `id` INTEGER UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `property` varchar(191) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `value` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  CONSTRAINT MASTER_DATA_UNIQUE1 UNIQUE (property)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO MASTER_DATA (property, value) VALUES 
  ('SANTHA_AMOUNT','100'),
  ('USER_ID_PREFIX','SOC_');
  
CREATE TABLE `USER_ROLE_MAPPING` (
  `id` INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `role_id` INTEGER NOT NULL,
  `access` varchar(70) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO USER_ROLE_MAPPING (role_id, access) VALUES 
  (2,'finance_read'),
  (2,'finance_write'),
  (1,'finance_write'),
  (1,'member_add'),
  (0,'member_dashboard'),
  (0,'member_list'),
  (3,'all');


CREATE TABLE `APP_USER` (
  `id` INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `name` varchar(70) NOT NULL,
  `role_id` INTEGER  DEFAULT 0 COMMENT '0=>user,1=>admin, 2=>finance, 3=>super admin',
  `user_name` varchar(70) NOT NULL,
  `image_path` varchar(255) DEFAULT NULL,
  `encrypted_password` varchar(255) NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `mobile` varchar(10) DEFAULT NULL,
  `created_on` datetime DEFAULT current_timestamp(),
  CONSTRAINT USERS_UNIQUE1 UNIQUE (name),
  CONSTRAINT USERS_UNIQUE2 UNIQUE (user_name),
  CONSTRAINT USERS_UNIQUE3 UNIQUE (mobile)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE `EMPLOYEES` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `employee_type` INTEGER UNSIGNED DEFAULT 0 COMMENT '0=>incharge',
  `name` varchar(50) NOT NULL,
  `DOB` DATE NOT NULL,
  `Gender` INTEGER UNSIGNED DEFAULT 0 COMMENT '0=>Male,1=>Female',
  `image_path` varchar(255) DEFAULT NULL,
  `Address` varchar(255) NOT NULL,
  `city` varchar(120) NOT NULL,
  `state` varchar(120) NOT NULL,
  `pincode` INTEGER NOT NULL,
  `Aadhar_no` bigint(20) NOT NULL,
  `Mobile_no` bigint(20) NOT NULL,
  `Join_date` DATE NOT NULL,
  `salary` DOUBLE NOT NULL,
  `relieving_date` varchar(10) DEFAULT NULL,
  `created_on` datetime DEFAULT current_timestamp()
  ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `MEMBER_PROFILE` (
  `id` bigint(20)  NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `user_id` varchar(50) NOT NULL,
  `name` varchar(50) NOT NULL,
  `DOB` DATE NOT NULL,
  `image_path` varchar(255) DEFAULT NULL,
  `gender` INTEGER UNSIGNED DEFAULT 0 COMMENT '0=>Male,1=>Female',
  `address` varchar(255) NOT NULL,
  `city` varchar(120) NOT NULL,
  `district` varchar(120) NOT NULL,
  `state` varchar(120) NOT NULL,
  `pincode` INTEGER NOT NULL,
  `auth_type_id` INTEGER NOT NULL DEFAULT 0 COMMENT '0=>Aadhar,1=>Driving etc',
  `auth_data` varchar(100) NOT NULL,
  `auth_path` varchar(255) DEFAULT NULL,
  `mobile_no` bigint(20) NOT NULL,
  `join_date` DATE NOT NULL,
  `santha_amount` DOUBLE DEFAULT NULL,
  `is_leader` INTEGER NOT NULL DEFAULT 0 COMMENT '0=>No,1=>Yes',
  `leader_id` bigint(20) DEFAULT NULL,
  `incharge_id` bigint(20) DEFAULT NULL,
  `status` INTEGER NOT NULL DEFAULT 0 COMMENT '0=>Active,1=>Closed,2=>Suspended',
  `last_status_change_date` DATE DEFAULT NULL,
  `comments` varchar(255) DEFAULT NULL,
  `nominee_name` varchar(255) DEFAULT NULL,
  `nominee_DOB` DATE NOT NULL,
  `nominee_relation` varchar(255) DEFAULT NULL,
  `nominee_mobile_number` bigint(20) DEFAULT NULL,
  `nominee_Aadhar_no` bigint(20) DEFAULT NULL,
  `created_on` datetime DEFAULT current_timestamp(),
  CONSTRAINT MEMBER_PROFILE_UNIQUE1 UNIQUE (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE `santha_payments` (
  `id` bigint(20)  NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `member_id` bigint(20) NOT NULL,
  `santha_for_year` INTEGER  NOT NULL,
  `santha_amount_received` DOUBLE NOT NULL,
  `received_date` DATE NOT NULL,
  `created_on` datetime DEFAULT current_timestamp(),
  CONSTRAINT `fk_santha_payments_member` FOREIGN KEY (member_id) REFERENCES MEMBER_PROFILE (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE `member_savings` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `member_id` bigint(20) NOT NULL,
  `date` DATE NOT NULL,
  `initial_amount` double NOT NULL,
  `payment_amount` double NOT NULL COMMENT 'This will be in negative for withdrawal',
  `final_balance` double NOT NULL,
  `created_by` datetime DEFAULT NULL,
  CONSTRAINT `fk_member_savings_member` FOREIGN KEY (member_id) REFERENCES MEMBER_PROFILE (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE `benefits` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `member_id` bigint(20) NOT NULL,
  `status` INTEGER NOT NULL DEFAULT 0 COMMENT '0=>Pending,1=>Approved,2=>Rejected',
  `benefit_type` varchar(50) NOT NULL,
  `approved_on` DATE NOT NULL,
  `approved_by` INTEGER DEFAULT NULL,
  `issued_on` DATE NOT NULL,
  `remarks` varchar(150) DEFAULT NULL,
  `created_on` datetime DEFAULT current_timestamp(),
  `reference_no` bigint(20) DEFAULT NULL,
  CONSTRAINT `fk_benefits_member` FOREIGN KEY (member_id) REFERENCES MEMBER_PROFILE (id),
  CONSTRAINT `fk_benefits_approval_user` FOREIGN KEY (approved_by) REFERENCES APP_USER (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `pension` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `member_id` bigint(20) NOT NULL,
  `status` INTEGER NOT NULL DEFAULT 0 COMMENT '0=>Pending,1=>Active,2=>Rejected,4=Closed',
  `pension_monthly_amount` double NOT NULL,
  `start_date` DATE NOT NULL,
  `end_date` DATE NOT NULL,
  `approved_by` INTEGER DEFAULT NULL,
  `remark` varchar(50) NOT NULL,
  `created_on` datetime DEFAULT current_timestamp(),
  `reference_no` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `pension_payment` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `member_id` bigint(20) DEFAULT NULL,
  `pension_id` bigint(20) DEFAULT NULL,
  `month` INTEGER NOT NULL,
  `year` INTEGER NOT NULL,
  `paid_date` DATE NOT NULL,
  `amount` double DEFAULT NULL,
  `created_by` datetime DEFAULT NULL,
  CONSTRAINT `fk_pension_payment_member` FOREIGN KEY (member_id) REFERENCES MEMBER_PROFILE (id),
  CONSTRAINT `fk_pension_payment_pension` FOREIGN KEY (pension_id) REFERENCES PENSION (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE `loan_request` (
  `id` bigint(20)  NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `requested_by` bigint(20) NOT NULL,
  `loan_amount` DOUBLE NOT NULL,
  `number_of_emi` INTEGER NOT NULL,
  `interest_rate` DOUBLE NOT NULL,
  `final_payable_amount` DOUBLE NOT NULL,
  `requested_loan_type` INTEGER NOT NULL DEFAULT 0 COMMENT '0=>Savings,1=>Business,2=>Education',
  `applied_on` DATE NOT NULL,
  `status` INTEGER NOT NULL DEFAULT 0 COMMENT '0=>Pending,1=>Approved,2=>Rejected',
  `comments` varchar(100) DEFAULT NULL,
  `action_by_user` INTEGER DEFAULT NULL COMMENT 'person who took the last action',
  `created_on` datetime DEFAULT current_timestamp(),
  CONSTRAINT `fk_loan_request_member` FOREIGN KEY (requested_by) REFERENCES MEMBER_PROFILE (id),
  CONSTRAINT `fk_loan_request_action_user` FOREIGN KEY (action_by_user) REFERENCES APP_USER (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE `savings_loans` (
  `id` bigint(20)  NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `member_id` bigint(20) NOT NULL,
  `status` INTEGER NOT NULL DEFAULT 0 COMMENT '0=>Active,1=>Closed,2=>Defaulted',
  `loan_amount` DOUBLE NOT NULL,
  `EMI_amount` DOUBLE NOT NULL,
  `interest_rate` DOUBLE NOT NULL,
  `final_payable_amount` DOUBLE NOT NULL,
  `monthly_penalty_amount` DOUBLE NOT NULL,
  `penalty_interest_percentage` DOUBLE NOT NU LL,
  `months_to_charge_penalty_interest` INTEGER DEFAULT NULL,
  `number_of_emi` INTEGER NOT NULL,
  `EMI_start_date` DATE NOT NULL,
  `loan_end_date` DATE NOT NULL,
  `emi_on_date` INTEGER NOT NULL COMMENT 'last day to pay emi every month',
  `comments` varchar(100) DEFAULT NULL,
  `loan_approved_by` INTEGER DEFAULT NULL,
  `created_on` datetime DEFAULT current_timestamp(),
  CONSTRAINT `fk_savings_loans_member` FOREIGN KEY (member_id) REFERENCES MEMBER_PROFILE (id),
  CONSTRAINT `fk_savings_loans_approval_user` FOREIGN KEY (loan_approved_by) REFERENCES APP_USER (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE `savings_loan_payment` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `member_id` bigint(20) DEFAULT NULL,
  `loan_id` bigint(20) DEFAULT NULL,
  `month` INTEGER NOT NULL,
  `year` INTEGER NOT NULL,
  `emi_count` INTEGER NOT NULL,
  `paid_date` DATE NOT NULL,
  `amount` double DEFAULT NULL,
  `created_by` datetime DEFAULT NULL,
  CONSTRAINT `fk_savings_loan_payment_member` FOREIGN KEY (member_id) REFERENCES MEMBER_PROFILE (id),
  CONSTRAINT `fk_savings_loan_payment_loan_id` FOREIGN KEY (loan_id) REFERENCES savings_loans (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `education_loans` (
  `id` bigint(20)  NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `member_id` bigint(20) NOT NULL,
  `status` INTEGER NOT NULL DEFAULT 0 COMMENT '0=>Active,1=>Closed,2=>Defaulted',
  `loan_amount` DOUBLE NOT NULL,
  `EMI_amount` DOUBLE NOT NULL,
  `monthly_penalty_amount` DOUBLE NOT NULL,
  `penalty_interest_percentage` DOUBLE NOT NULL,
  `months_to_charge_penalty_interest` INTEGER DEFAULT NULL,
  `number_of_emi` INTEGER NOT NULL,
  `EMI_start_date` DATE NOT NULL,
  `loan_end_date` DATE NOT NULL,
  `emi_on_date` INTEGER NOT NULL COMMENT 'last day to pay emi every month',
  `comments` varchar(100) DEFAULT NULL,
  `loan_approved_by` INTEGER DEFAULT NULL,
  `created_on` datetime DEFAULT current_timestamp(),
  CONSTRAINT `fk_education_loans_member` FOREIGN KEY (member_id) REFERENCES MEMBER_PROFILE (id),
  CONSTRAINT `fk_education_loans_approval_user` FOREIGN KEY (loan_approved_by) REFERENCES APP_USER (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `education_loan_payment` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `member_id` bigint(20) DEFAULT NULL,
  `loan_id` bigint(20) DEFAULT NULL,
  `month` INTEGER NOT NULL,
  `year` INTEGER NOT NULL,
  `emi_count` INTEGER NOT NULL,
  `paid_date` DATE NOT NULL,
  `amount` double DEFAULT NULL,
  `created_by` datetime DEFAULT NULL,
  CONSTRAINT `fk_education_loan_payment_member` FOREIGN KEY (member_id) REFERENCES MEMBER_PROFILE (id),
  CONSTRAINT `fk_education_loan_payment_loan_id` FOREIGN KEY (loan_id) REFERENCES education_loans (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `business_loans` (
  `id` bigint(20)  NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `member_id` bigint(20) NOT NULL,
  `status` INTEGER NOT NULL DEFAULT 0 COMMENT '0=>Active,1=>Closed,2=>Defaulted',
  `loan_amount` DOUBLE NOT NULL,
  `EMI_amount` DOUBLE NOT NULL,
  `monthly_penalty_amount` DOUBLE NOT NULL,
  `penalty_interest_percentage` DOUBLE NOT NULL,
  `months_to_charge_penalty_interest` INTEGER DEFAULT NULL,
  `number_of_emi` INTEGER NOT NULL,
  `EMI_start_date` DATE NOT NULL,
  `loan_end_date` DATE NOT NULL,
  `emi_on_date` INTEGER NOT NULL COMMENT 'last day to pay emi every month',
  `comments` varchar(100) DEFAULT NULL,
  `loan_approved_by` INTEGER DEFAULT NULL,
  `created_on` datetime DEFAULT current_timestamp(),
  CONSTRAINT `fk_business_loans_member` FOREIGN KEY (member_id) REFERENCES MEMBER_PROFILE (id),
  CONSTRAINT `fk_business_loans_approval_user` FOREIGN KEY (loan_approved_by) REFERENCES APP_USER (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `business_loan_payment` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `member_id` bigint(20) DEFAULT NULL,
  `loan_id` bigint(20) DEFAULT NULL,
  `month` INTEGER NOT NULL,
  `year` INTEGER NOT NULL,
  `emi_count` INTEGER NOT NULL,
  `paid_date` DATE NOT NULL,
  `amount` double DEFAULT NULL,
  `created_by` datetime DEFAULT NULL,
  CONSTRAINT `fk_business_loan_payment_member` FOREIGN KEY (member_id) REFERENCES MEMBER_PROFILE (id),
  CONSTRAINT `fk_business_loan_payment_loan_id` FOREIGN KEY (loan_id) REFERENCES business_loans (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE CATAGORY_SUBCATAGORY (
	`id` Integer  NOT NULL AUTO_INCREMENT PRIMARY KEY,
	`CATAGORY` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
	`SUBCATAGORY` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
    CONSTRAINT CATAGORY_UNIQUE UNIQUE (CATAGORY,SUBCATAGORY)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

insert into CATAGORY_SUBCATAGORY (CATAGORY,SUBCATAGORY) values ('TRAVEL','Team 1');

CREATE TABLE `expense` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `amount` double NOT NULL,
  `paid_to` varchar(100) DEFAULT NULL,
  `ref_no` varchar(255) DEFAULT NULL,
  `category_id` INTEGER NOT NULL,
  `description` varchar(250) DEFAULT NULL,
  `paid_date` DATE NOT NULL,
  `created_date` datetime DEFAULT current_timestamp(),
  CONSTRAINT `fk_expense_category` FOREIGN KEY (category_id) REFERENCES CATAGORY_SUBCATAGORY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `income` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `amount` double NOT NULL,
  `received_from` varchar(100) DEFAULT NULL,
  `ref_no` varchar(255) DEFAULT NULL,
  `category_id` INTEGER NOT NULL,
  `description` varchar(250) DEFAULT NULL,
  `received_date` DATE NOT NULL,
  `created_date` datetime DEFAULT current_timestamp(),
  CONSTRAINT `fk_income_category` FOREIGN KEY (category_id) REFERENCES CATAGORY_SUBCATAGORY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE `BANK_ACCOUNTS` (
  `id` INTEGER  NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `acc_number` varchar(191) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `account_name` varchar(191) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `name` varchar(191) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `branch` varchar(191) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `IFSC_code` varchar(191) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `BANK_TRANSACTIONS` (
  `id` bigint(20)  NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `bank_id` INTEGER UNSIGNED NOT NULL,
  `transfer_type` varchar(191) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'Online or In Bank',
  `transaction_type` INTEGER UNSIGNED DEFAULT 0 COMMENT '0=>Deposit,1=>WithDrawal',
  `transaction_date` DATE NOT NULL,
  `amount` Double UNSIGNED NOT NULL,
  `deposited_by` varchar(191) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `reference_no` varchar(191) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `comments` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT `fk_transactions_bank` FOREIGN KEY (bank_id) REFERENCES BANK_ACCOUNTS (id)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `payable` (
  `id` bigint(20)  NOT NULL AUTO_INCREMENT PRIMARY KEY,
   `ref_no` varchar(255) NOT NULL,
   `category_id` INTEGER NOT NULL,
  `description` varchar(250) DEFAULT NULL,
  `amount` double NOT NULL,
  `to_whom` varchar(100) DEFAULT NULL,
  `due_date` DATE NOT NULL,
  `status` INTEGER UNSIGNED DEFAULT 0 COMMENT '0=>not paid,1=>paid',
  `created_date` datetime DEFAULT current_timestamp(),
  CONSTRAINT `fk_payable_category` FOREIGN KEY (category_id) REFERENCES CATAGORY_SUBCATAGORY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE `receivable` (
 `id` bigint(20)  NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `ref_no` varchar(255) NOT NULL,
  `category_id` INTEGER NOT NULL,
  `description` varchar(250) DEFAULT NULL,
  `amount` double NOT NULL,
  `from_whom` varchar(100) DEFAULT NULL,
  `due_date` DATE NOT NULL,
  `status` INTEGER UNSIGNED DEFAULT 0 COMMENT '0=>not received,1=>received',
  `created_date` datetime DEFAULT current_timestamp(),
  CONSTRAINT `fk_receivable_category` FOREIGN KEY (category_id) REFERENCES CATAGORY_SUBCATAGORY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;





