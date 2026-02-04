// 轮播图功能
document.addEventListener('DOMContentLoaded', function() {
  const sliderWrapper = document.querySelector('.slider-wrapper');
  const sliderItems = document.querySelectorAll('.slider-item');
  const prevBtn = document.getElementById('prevBtn');
  const nextBtn = document.getElementById('nextBtn');
  const dots = document.querySelectorAll('.dot');
  
  let currentIndex = 0;
  const totalSlides = sliderItems.length;
  let autoPlayInterval;
  
  // 初始化
  function init() {
    if (totalSlides === 0) return;
    
    // 设置每个轮播项的初始动画
    sliderItems.forEach((item, index) => {
      item.style.display = index === 0 ? 'block' : 'none';
    });
    
    // 绑定事件
    bindEvents();
    
    // 开始自动播放
    startAutoPlay();
  }
  
  // 绑定事件
  function bindEvents() {
    if (prevBtn) {
      prevBtn.addEventListener('click', () => {
        goToSlide(currentIndex - 1);
        resetAutoPlay();
      });
    }
    
    if (nextBtn) {
      nextBtn.addEventListener('click', () => {
        goToSlide(currentIndex + 1);
        resetAutoPlay();
      });
    }
    
    dots.forEach((dot, index) => {
      dot.addEventListener('click', () => {
        goToSlide(index);
        resetAutoPlay();
      });
    });
    
    // 键盘控制
    document.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowLeft') {
        goToSlide(currentIndex - 1);
        resetAutoPlay();
      } else if (e.key === 'ArrowRight') {
        goToSlide(currentIndex + 1);
        resetAutoPlay();
      }
    });
    
    // 触摸滑动支持
    let touchStartX = 0;
    let touchEndX = 0;
    
    const sliderContainer = document.querySelector('.slider-container');
    
    sliderContainer.addEventListener('touchstart', (e) => {
      touchStartX = e.changedTouches[0].screenX;
      stopAutoPlay();
    }, { passive: true });
    
    sliderContainer.addEventListener('touchend', (e) => {
      touchEndX = e.changedTouches[0].screenX;
      handleSwipe();
      startAutoPlay();
    }, { passive: true });
    
    function handleSwipe() {
      const diff = touchStartX - touchEndX;
      const threshold = 50;
      
      if (Math.abs(diff) > threshold) {
        if (diff > 0) {
          // 向左滑动，显示下一个
          goToSlide(currentIndex + 1);
        } else {
          // 向右滑动，显示上一个
          goToSlide(currentIndex - 1);
        }
      }
    }
    
    // 鼠标悬停时暂停自动播放
    const heroSlider = document.querySelector('.hero-slider');
    heroSlider.addEventListener('mouseenter', stopAutoPlay);
    heroSlider.addEventListener('mouseleave', startAutoPlay);
  }
  
  // 切换到指定幻灯片
  function goToSlide(index) {
    if (index < 0) {
      currentIndex = totalSlides - 1;
    } else if (index >= totalSlides) {
      currentIndex = 0;
    } else {
      currentIndex = index;
    }
    
    updateSlider();
  }
  
  // 更新轮播显示
  function updateSlider() {
    // 隐藏所有幻灯片
    sliderItems.forEach((item, index) => {
      if (index === currentIndex) {
        item.style.display = 'block';
        // 触发动画
        const text = item.querySelector('.slider-text');
        text.style.animation = 'none';
        text.offsetHeight; // 触发回流
        text.style.animation = 'slideUp 0.8s ease-out';
      } else {
        item.style.display = 'none';
      }
    });
    
    // 更新圆点状态
    dots.forEach((dot, index) => {
      dot.classList.toggle('active', index === currentIndex);
    });
    
    // 更新按钮状态
    if (prevBtn) {
      prevBtn.style.opacity = currentIndex === 0 ? '0.5' : '1';
      prevBtn.style.cursor = currentIndex === 0 ? 'not-allowed' : 'pointer';
    }
    
    if (nextBtn) {
      nextBtn.style.opacity = currentIndex === totalSlides - 1 ? '0.5' : '1';
      nextBtn.style.cursor = currentIndex === totalSlides - 1 ? 'not-allowed' : 'pointer';
    }
  }
  
  // 自动播放
  function startAutoPlay() {
    stopAutoPlay();
    autoPlayInterval = setInterval(() => {
      goToSlide(currentIndex + 1);
    }, 5000); // 5秒自动切换
  }
  
  function stopAutoPlay() {
    if (autoPlayInterval) {
      clearInterval(autoPlayInterval);
    }
  }
  
  function resetAutoPlay() {
    stopAutoPlay();
    startAutoPlay();
  }
  
  // 初始化轮播
  init();
});
