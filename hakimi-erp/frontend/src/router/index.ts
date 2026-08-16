import { createRouter, createWebHistory } from "vue-router"
import MainLayout from "@/layout/MainLayout.vue"
import { getAuthToken } from "@/utils/auth"

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/login",
      name: "Login",
      component: () => import("@/views/auth/LoginView.vue"),
      meta: { title: "Sign In", public: true },
    },
    {
      path: "/register",
      name: "Register",
      component: () => import("@/views/auth/RegisterView.vue"),
      meta: { title: "Create Account", public: true },
    },
    {
      path: "/",
      component: MainLayout,
      meta: { requiresAuth: true },
      children: [
        { path: "", name: "Home", component: () => import("@/views/Home.vue"), meta: { title: "Home" } },
        { path: "customer/bp", name: "BusinessPartner", component: () => import("@/views/customer/BusinessPartner.vue"), meta: { title: "Create Business Partner" } },
        { path: "customer/material", name: "Material", component: () => import("@/views/customer/MaterialMaster.vue"), meta: { title: "Material Master" } },
        { path: "customer/product", name: "Product", component: () => import("@/views/customer/Product.vue"), meta: { title: "Product" } },
        { path: "customer/pricing", name: "Pricing", component: () => import("@/views/customer/PricingConditions.vue"), meta: { title: "Pricing Conditions" } },
        { path: "customer/salesorg", name: "SalesOrg", component: () => import("@/views/customer/SalesOrganization.vue"), meta: { title: "Sales Organization" } },
        { path: "sales/inquiry", name: "InquiryManagement", component: () => import("@/views/sales/InquiryManagement.vue"), meta: { title: "Inquiry Management" } },
        { path: "sales/inquiry/new", name: "CreateInquiry", component: () => import("@/views/sales/InquiryItem.vue"), meta: { title: "Create Inquiry" } },
        { path: "sales/inquiry/:id", name: "InquiryDetail", component: () => import("@/views/sales/InquiryItem.vue"), meta: { title: "Inquiry Details" } },
        { path: "sales/quotation", name: "QuotationManagement", component: () => import("@/views/sales/QuotationManagement.vue"), meta: { title: "Quotation Management" } },
        { path: "sales/quotation/new", name: "CreateQuotation", component: () => import("@/views/sales/QuotationItem.vue"), meta: { title: "Create Quotation" } },
        { path: "sales/quotation/:id", name: "QuotationDetail", component: () => import("@/views/sales/QuotationItem.vue"), meta: { title: "Quotation Details" } },
        { path: "sales/orders", name: "SalesOrders", component: () => import("@/views/sales/SalesOrders.vue"), meta: { title: "Sales Orders" } },
        { path: "sales/orders/new", name: "CreateOrder", component: () => import("@/views/sales/SalesOrderDetail.vue"), meta: { title: "Create Order" } },
        { path: "sales/order/:id", name: "OrderDetail", component: () => import("@/views/sales/SalesOrderDetail.vue"), meta: { title: "Order Details" } },
        { path: "delivery/list", name: "DeliveryList", component: () => import("@/views/delivery/DeliveryList.vue"), meta: { title: "Delivery List" } },
        { path: "delivery/monitor", name: "DeliveryMonitor", component: () => import("@/views/delivery/StatusMonitor.vue"), meta: { title: "Delivery Status Monitoring" } },
        { path: "delivery/detail/:id", name: "DeliveryDetail", component: () => import("@/views/delivery/DeliveryDetail.vue"), meta: { title: "Delivery Details" } },
        { path: "finance/invoice", name: "InvoiceManagement", component: () => import("@/views/finance/InvoiceManagement.vue"), meta: { title: "Invoice Management" } },
        { path: "finance/receivables", name: "ReceivablesManagement", component: () => import("@/views/finance/ReceivablesManagement.vue"), meta: { title: "Receivables Management" } },
        { path: "finance/unpaid", name: "UnpaidReceivables", component: () => import("@/views/finance/UnpaidReceivables.vue"), meta: { title: "Unpaid Accounts Receivable" } },
        { path: "finance/receivable/:id", name: "ReceivableDetail", component: () => import("@/views/finance/ReceivableDetail.vue"), meta: { title: "Receivable Details" } },
        { path: "report", name: "Report", component: () => import("@/views/report/ReportQuery.vue"), meta: { title: "Report Query" } },
        { path: "settings", name: "Settings", component: () => import("@/views/settings/SystemSettings.vue"), meta: { title: "System Settings" } },
      ]
    }
  ]
})

router.beforeEach((to) => {
  const authenticated = Boolean(getAuthToken())

  if (to.meta.requiresAuth && !authenticated) {
    return {
      path: "/login",
      query: { redirect: to.fullPath },
    }
  }

  if (to.meta.public && authenticated) {
    return "/"
  }

  return true
})

export default router
