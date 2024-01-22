import { createRouter, createWebHistory } from "vue-router";
import LoginComponent from "@/components/LoginComponent.vue";
import RegisterComponent from "@/components/RegisterComponent.vue";
import FrontpageComponent from "@/components/FrontpageComponent.vue";
import LoginmanagerComponent from "@/components/LoginmanagerComponent.vue";
import PurchaseComponent from "@/components/PurchaseComponent.vue";
import AdditemComponent from "@/components/AdditemComponent.vue";
import LoginadminComponent from "@/components/LoginadminComponent.vue";
import AddcategoryComponent from "@/components/AddcategoryComponent.vue";
import LogoutComponent from "@/components/LogoutComponent.vue";
import AdminDashboard from "@/components/AdminDashboard.vue";
import ViewCart from "@/components/ViewCart.vue";
import SearchComponent from "@/components/SearchComponent.vue";
import UserprofileComponent from "@/components/UserprofileComponent.vue";
import ViewCategory from "@/components/ViewCategory.vue";
import DeleteUser from "@/components/DeleteUser.vue";
import RatingComponent from "@/components/RatingComponent.vue";
import ProductDetailsComponent from "@/components/ProductDetailsComponent.vue";
import ManagerDashboard from "@/components/ManagerDashboard.vue";
import DeleteProduct from "@/components/DeleteProduct.vue";
import UpdatecategoryRequest from "@/components/UpdatecategoryRequest.vue";
import UpdateCategory from "@/components/UpdateCategory.vue";
import DeleteCategory from "@/components/DeleteCategory.vue";
import DeletecategoryAdmin from "@/components/DeletecategoryAdmin.vue";
import UpdatecategoryAdmin from "@/components/UpdatecategoryAdmin.vue";
const routes = [
  {
    path: "/category/:categoryId",
    name: "category", // This should match the name used in this.$router.push
    component: ViewCategory,
  },
  {
    path: "/product/:id",
    name: "productDetails",
    component: ProductDetailsComponent,
  },
  {
    path: "/product/:id/ratings",
    name: "product-ratings",
    component: RatingComponent,
    props: true,
  },
  { path: "/delete_user", component: DeleteUser },
  {
    path: "/delete_product/:id",
    name: "deleteProduct",
    component: DeleteProduct,
    props: true, // Automatically pass route params as props to the component
  },
  {
    path: "/",
    name: "frontpage",
    component: FrontpageComponent,
  },
  {
    path: "/register_user",
    name: "register",
    component: RegisterComponent,
  },
  {
    path: "/login_admin",
    name: "loginadmin",
    component: LoginadminComponent,
  },
  {
    path: "/login_customer",
    name: "logincustomer",
    component: LoginComponent,
  },
  {
    path: "/login_manager",
    name: "loginmanager",
    component: LoginmanagerComponent,
  },
  {
    path: "/add_category",
    name: "addcategory",
    component: AddcategoryComponent,
  },
  {
    path: "/add_item",
    name: "additem",
    component: AdditemComponent,
  },
  {
    path: "/logout",
    name: "logout",
    component: LogoutComponent,
  },
  {
    path: "/admin_dashboard",
    name: "adminDashboard",
    component: AdminDashboard,
  },
  { path: "/manager_dashboard", component: ManagerDashboard },
  {
    path: "/add_to_cart",
    name: "purchase",
    component: PurchaseComponent,
  },
  {
    path: "/view_cart",
    name: "ViewCart",
    component: ViewCart,
  },
  {
    path: "/search",
    name: "Search",
    component: SearchComponent,
  },
  {
    path: "/product/:id",
    name: "productDetails",
    component: ProductDetailsComponent,
  },
  { path: "/user_profile", component: UserprofileComponent },
  {
    path: "/update_category_request/:categoryId",
    name: "updateCategoryRequest", // Make sure to give it a name
    component: UpdatecategoryRequest,
  },
  {
    path: "/update_category_admin/:categoryId",
    name: "updateCategoryAdmin", // Make sure to give it a name
    component: UpdatecategoryAdmin,
  },
  {
    path: "/update_category/:categoryId",
    name: "updateCategory", // Make sure to give it a name
    component: UpdateCategory,
  },
  {
    path: "/delete_category_admin/:id",
    name: "deleteCategoryAdmin",
    component: DeletecategoryAdmin,
  },
  {
    path: "/delete_category_request/:id",
    name: "deleteCategory",
    component: DeleteCategory,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
