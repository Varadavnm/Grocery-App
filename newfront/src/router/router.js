import { createRouter, createWebHistory } from "vue-router";
import LoginComponent from "@/components/loginComponent.vue";
import LoginmanagerComponent from "@/components/loginmanagerComponent.vue";
import RegisterComponent from "@/components/RegisterComponent.vue";
import PurchaseComponent from "@/components/PurchaseComponent.vue";
import FrontpageComponent from "@/components/FrontpageComponent.vue";
import AdditemComponent from "@/components/AdditemComponent.vue";
import LoginadminComponent from "@/components/LoginadminComponent.vue";
import LogoutComponent from "@/components/LogoutComponent.vue";
import ViewCart from "@/components/ViewCart.vue";
import UpdateComponent from "@/components/UpdateComponent.vue";
import UserprofileComponent from "@/components/UserprofileComponent.vue";
import ViewCategory from "@/components/ViewCategory.vue";
import DeleteUser from "@/components/DeleteUser.vue";
import SearchComponent from "@/components/SearchComponent.vue";
import RatingComponent from "@/components/RatingComponent.vue";
import ProductDetailsComponent from "@/components/RatingComponent.vue";
import ManagerDashboard from "@/components/ManagerDashboard.vue";
import DeleteProduct from "@/components/DeleteProduct.vue";
import UpdatecategoryRequest from "@/components/UpdatecategoryRequest.vue";
import UpdateCategory from "@/components/UpdateCategory.vue";
import DeleteCategory from "@/components/DeelteCategory.vue";
import DeletecategoryAdmin from "@/components/DeeltecategoryAdmin.vue";
import UpdatecategoryAdmin from "@/components/UpdatecategoryAdmin.vue";
const routes = [
  { path: "/", component: FrontpageComponent },
  {
    path: "/product/:id/ratings",
    name: "product-ratings",
    component: RatingComponent,
    props: true,
  },
  { path: "/manager_dashboard", component: ManagerDashboard },
  {
    path: "/delete_category_request/:id",
    name: "deleteCategory",
    component: DeleteCategory,
  },
  {
    path: "/delete_category_admin/:id",
    name: "deleteCategoryAdmin",
    component: DeletecategoryAdmin,
  },
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
  { path: "/login_admin", component: LoginadminComponent },
  { path: "/login_customer", component: LoginComponent },
  { path: "/login_manager", component: LoginmanagerComponent },
  { path: "/register_user", component: RegisterComponent },
  { path: "/add_to_cart", component: PurchaseComponent },
  { path: "/add_item", component: AdditemComponent },
  { path: "/logout", component: LogoutComponent },
  { path: "/view_cart", component: ViewCart },
  { path: "/user_profile", component: UserprofileComponent },
  { path: "/update_profile", component: UpdateComponent },
  { path: "/delete_user", component: DeleteUser },
  {
    path: "/delete_product/:id",
    name: "delete_product",
    component: DeleteProduct,
    props: true,
  },
  {
    path: "/update_category_request/:categoryId",
    name: "updateCategoryRequest", // Make sure to give it a name
    component: UpdatecategoryRequest,
  },
  {
    path: "/update_category/:categoryId",
    name: "updateCategory", // Make sure to give it a name
    component: UpdateCategory,
  },
  {
    path: "/update_category_admin/:categoryId",
    name: "updateCategoryAdmin", // Make sure to give it a name
    component: UpdatecategoryAdmin,
  },
  {
    path: "/search",
    name: "Search",
    component: SearchComponent,
  },
  // {
  //   path: "/product/:id",
  //   component: ProductDetailsComponent,
  // },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
