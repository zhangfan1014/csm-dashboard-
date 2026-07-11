-- ==========================================
-- CSM客户看板 · 数据库初始化
-- 在 Supabase SQL Editor 里运行此脚本
-- ==========================================

-- 1. 创建 customers 表
CREATE TABLE customers (
  id BIGSERIAL PRIMARY KEY,
  -- 基础信息（来自CRM）
  客户名称 TEXT,
  客户等级 TEXT,
  经营模式 TEXT,
  买断年费 TEXT,
  最近合同到期 TEXT,
  最近拜访日期 TEXT,
  拜访概要 TEXT,
  对应销售 TEXT,
  
  -- CRM原始字段
  ownerId_name TEXT,
  industryId_label TEXT,
  customItem187__c_label TEXT,
  customItem207__c_label TEXT,
  customItem263__c_formatted TEXT,
  customItem264__c_formatted TEXT,
  expireTime_formatted TEXT,
  customItem214__c_formatted TEXT,
  comment TEXT,
  customItem319__c_label TEXT,
  customItem305__c_label TEXT,
  customItem318__c TEXT,
  
  -- Excel原始字段
  client_level TEXT,
  sales_model TEXT,
  buyout_annual TEXT,
  first_sign_date TEXT,
  contract_end TEXT,
  visit_date TEXT,
  visit_record TEXT,
  summary TEXT,
  business_overview TEXT,
  visit_address TEXT,
  product_version TEXT,
  value_added_modules TEXT,
  sales_person TEXT,
  service_group TEXT,
  kp_contact TEXT,
  specific_person TEXT,
  
  -- 自定义字段（用于前端输入）
  custom_note TEXT,
  custom_tag TEXT,
  
  -- 字段供未来扩展
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. 开启 RLS（Row Level Security）
ALTER TABLE customers ENABLE ROW LEVEL SECURITY;

-- 3. 创建公开读策略（前端通过 anon key 读取）
CREATE POLICY "允许公开读取" ON customers
  FOR SELECT USING (true);

-- 4. 创建公开写策略（前端通过 anon key 写入自定义字段）
CREATE POLICY "允许更新自定义字段" ON customers
  FOR UPDATE USING (true)
  WITH CHECK (true);

-- 5. 允许插入（数据同步用）
CREATE POLICY "允许插入" ON customers
  FOR INSERT WITH CHECK (true);

-- 6. 删除策略（用于数据重刷）
CREATE POLICY "允许删除" ON customers
  FOR DELETE USING (true);
