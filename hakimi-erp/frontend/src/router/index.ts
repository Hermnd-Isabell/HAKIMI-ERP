import { createRouter, createWebHistory } from "vue-router"

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/", name: "Home", component: () => import("@/views/Home.vue"), meta: { title: "Home" } },
    { path: "/customer/bp", name: "BusinessPartner", component: () => import("@/views/customer/BusinessPartner.vue"), meta: { title: "Create Business Partner" } },
    { path: "/customer/material", name: "Material", component: () => import("@/views/customer/MaterialMaster.vue"), meta: { title: "Material Master" } },
    { path: "/customer/product", name: "Product", component: () => import("@/views/customer/Product.vue"), meta: { title: "Product" } },
    { path: "/customer/pricing", name: "Pricing", component: () => import("@/views/customer/PricingConditions.vue"), meta: { title: "Pricing Conditions" } },
    { path: "/customer/salesorg", name: "SalesOrg", component: () => import("@/views/customer/SalesOrganization.vue"), meta: { title: "Sales Organization" } },
    { path: "/sales/inquiry", name: "InquiryManagement", component: () => import("@/views/sales/InquiryManagement.vue"), meta: { title: "Inquiry Management" } },
    { path: "/sales/quotation", name: "QuotationManagement", component: () => import("@/views/sales/QuotationManagement.vue"), meta: { title: "Quotation Management" } },
    { path: "/sales/quotation/new", name: "CreateQuotation", component: () => import("@/views/sales/QuotationItem.vue"), meta: { title: "Create Quotation" } },
    { path: "/sales/quotation/:id", name: "QuotationDetail", component: () => import("@/views/sales/QuotationItem.vue"), meta: { title: "Quotation Details" } },
    { path: "/sales/orders", name: "SalesOrders", component: () => import("@/views/sales/SalesOrders.vue"), meta: { title: "Sales Orders" } },
    { path: "/delivery/list", name: "DeliveryList", component: () => import("@/views/delivery/DeliveryList.vue"), meta: { title: "Delivery List" } },
    { path: "/delivery/monitor", name: "DeliveryMonitor", component: () => import("@/views/delivery/StatusMonitor.vue"), meta: { title: "Delivery Status Monitoring" } },
    { path: "/delivery/detail/:id", name: "DeliveryDetail", component: () => import("@/views/delivery/DeliveryDetail.vue"), meta: { title: "Delivery Details" } },
    { path: "/finance/invoice", name: "InvoiceManagement", component: () => import("@/views/finance/InvoiceManagement.vue"), meta: { title: "Invoice Management" } },
    { path: "/finance/receivables", name: "ReceivablesManagement", component: () => import("@/views/finance/ReceivablesManagement.vue"), meta: { title: "Receivables Management" } },
    { path: "/finance/unpaid", name: "UnpaidReceivables", component: () => import("@/views/finance/UnpaidReceivables.vue"), meta: { title: "Unpaid Accounts Receivable" } },
    { path: "/finance/receivable/:id", name: "ReceivableDetail", component: () => import("@/views/finance/ReceivableDetail.vue"), meta: { title: "Receivable Details" } },
    { path: "/report", name: "Report", component: () => import("@/views/report/ReportQuery.vue"), meta: { title: "Report Query" } },
    { path: "/settings", name: "Settings", component: () => import("@/views/settings/SystemSettings.vue"), meta: { title: "System Settings" } },
  ]
})

export default router
