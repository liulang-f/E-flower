<template>
  <footer class="admin-footer">
    <div class="footer-content">
      <p>&copy; {{ currentYear }} FlowerShop Admin Dashboard. All rights reserved.</p>
      <div class="footer-links">
        <a href="#">Privacy Policy</a>
        <a href="#">Terms of Service</a>
        <a href="#">Help Center</a>
      </div>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'AdminFooter',
  data() {
    return {
      currentYear: new Date().getFullYear()
    }
  }
}
</script>

<style scoped>
.admin-footer {
  background-color: #f8f9fa;
  padding: 15px 20px;
  border-top: 1px solid #e9ecef;
  margin-left: 250px;
  transition: margin 0.3s;
}

.footer-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
}

.footer-links a {
  margin-left: 15px;
  color: #6c757d;
  text-decoration: none;
}

.footer-links a:hover {
  color: #4a6b57;
}

.collapsed + .admin-footer {
  margin-left: 80px;
}
</style>