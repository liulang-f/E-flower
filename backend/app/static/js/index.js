/**
 * index.js - 首页特有JavaScript
 */

// DOM 加载完成后执行
document.addEventListener('DOMContentLoaded', function() {
    // 初始化轮播图
    initSlider();

    // 加载促销信息
    loadPromoFlowers();

    // 加载热门推荐
    loadPopularFlowers();

    // 加载新品上架
    loadNewFlowers();

    // 加载场景推荐
    loadScenarios();

    // 绑定购物车按钮事件
    bindAddToCartButtons();
});

/**
 * 初始化轮播图
 */
function initSlider() {
    // 获取轮播图数据（实际应从API获取）
    const banners = [
        {
            id: 1,
            image: 'static/images/banner1.jpg',
            title: '春季特惠，全场8折',
            description: '精选鲜花花束，为您的春日增添一抹色彩',
            link: 'flower-list.html?promotion=spring'
        },
        {
            id: 2,
            image: 'static/images/banner2.jpg',
            title: '母亲节特别礼盒',
            description: '为母亲准备一份特别的礼物，表达您的爱与感谢',
            link: 'flower-list.html?scenario=mothersday'
        },
        {
            id: 3,
            image: 'static/images/banner3.jpg',
            title: '办公室绿植系列',
            description: '为工作环境增添生机，提升办公质量',
            link: 'flower-list.html?category=plant'
        }
    ];

    // 初始化轮播图
    renderSlider(banners);
}

/**
 * 渲染轮播图
 * @param {Array} banners 轮播图数据
 */
function renderSlider(banners) {
    const sliderWrapper = document.getElementById('sliderWrapper');
    const sliderDots = document.getElementById('sliderDots');

    if (!sliderWrapper || !sliderDots || !banners.length) return;

    // 清空现有内容
    sliderWrapper.innerHTML = '';
    sliderDots.innerHTML = '';

    // 创建轮播图项
    banners.forEach((banner, index) => {
        // 创建轮播图项
        const sliderItem = document.createElement('div');
        sliderItem.className = 'slider-item';
        sliderItem.innerHTML = `
            <a href="${banner.link}">
                <img src="${banner.image}" alt="${banner.title}">
                <div class="slider-item-content">
                    <h3>${banner.title}</h3>
                    <p>${banner.description}</p>
                </div>
            </a>
        `;
        sliderWrapper.appendChild(sliderItem);

        // 创建指示点
        const dot = document.createElement('div');
        dot.className = `slider-dot ${index === 0 ? 'active' : ''}`;
        dot.dataset.index = index;
        sliderDots.appendChild(dot);
    });

    // 设置容器宽度
    sliderWrapper.style.width = `${100 * banners.length}%`;

    // 初始化轮播功能
    let currentIndex = 0;
    const totalSlides = banners.length;

    // 切换到指定页
    function goToSlide(index) {
        currentIndex = index;
        sliderWrapper.style.transform = `translateX(-${(100 / totalSlides) * currentIndex}%)`;

        // 更新指示点状态
        const dots = sliderDots.querySelectorAll('.slider-dot');
        dots.forEach((dot, i) => {
            dot.classList.toggle('active', i === currentIndex);
        });
    }

    // 切换到下一页
    function nextSlide() {
        goToSlide((currentIndex + 1) % totalSlides);
    }

    // 切换到上一页
    function prevSlide() {
        goToSlide((currentIndex - 1 + totalSlides) % totalSlides);
    }

    // 添加指示点点击事件
    sliderDots.addEventListener('click', function(e) {
        if (e.target.classList.contains('slider-dot')) {
            const index = parseInt(e.target.dataset.index);
            goToSlide(index);
            resetAutoSlide(); // 重置自动切换计时器
        }
    });

    // 添加箭头点击事件
    document.getElementById('prevArrow').addEventListener('click', function() {
        prevSlide();
        resetAutoSlide();
    });

    document.getElementById('nextArrow').addEventListener('click', function() {
        nextSlide();
        resetAutoSlide();
    });

    // 自动轮播
    let slideInterval = setInterval(nextSlide, 5000);

    function resetAutoSlide() {
        clearInterval(slideInterval);
        slideInterval = setInterval(nextSlide, 5000);
    }

    // 鼠标悬停暂停轮播
    const sliderContainer = document.querySelector('.slider-container');
    sliderContainer.addEventListener('mouseenter', function() {
        clearInterval(slideInterval);
    });

    sliderContainer.addEventListener('mouseleave', function() {
        resetAutoSlide();
    });
}

/**
 * 加载促销花卉
 */
function loadPromoFlowers() {
    // 获取促销花卉数据（实际应从API获取）
    const promoFlowers = [
        {
            id: 101,
            name: '红玫瑰11枝礼盒',
            image: 'static/images/promo1.jpg',
            originalPrice: 199,
            price: 159,
            discount: '8折',
            endTime: '2025-03-30 23:59:59'
        },
        {
            id: 102,
            name: '向日葵花束',
            image: 'static/images/promo2.jpg',
            originalPrice: 168,
            price: 128,
            discount: '7.6折',
            endTime: '2025-03-25 23:59:59'
        },
        {
            id: 103,
            name: '百合花礼盒',
            image: 'static/images/promo3.jpg',
            originalPrice: 258,
            price: 198,
            discount: '7.7折',
            endTime: '2025-03-28 23:59:59'
        },
        {
            id: 104,
            name: '混合鲜花礼篮',
            image: 'static/images/promo4.jpg',
            originalPrice: 328,
            price: 268,
            discount: '8.2折',
            endTime: '2025-03-22 23:59:59'
        }
    ];

    // 渲染促销花卉
    renderPromoFlowers(promoFlowers);
}

/**
 * 渲染促销花卉
 * @param {Array} flowers 促销花卉数据
 */
function renderPromoFlowers(flowers) {
    const promoContainer = document.getElementById('promoContainer');
    if (!promoContainer || !flowers.length) return;

    // 清空现有内容
    promoContainer.innerHTML = '';

    // 创建促销花卉卡片
    flowers.forEach(flower => {
        const promoCard = document.createElement('div');
        promoCard.className = 'promo-card';
        promoCard.innerHTML = `
            <a href="flower-detail.html?id=${flower.id}">
                <div class="promo-image">
                    <img src="${flower.image}" alt="${flower.name}">
                    <div class="promo-discount">${flower.discount}</div>
                </div>
                <div class="promo-content">
                    <h3 class="promo-title">${flower.name}</h3>
                    <div class="promo-price">
                        <div class="current-price">${formatPrice(flower.price)}</div>
                        <div class="original-price">${formatPrice(flower.originalPrice)}</div>
                    </div>
                    <div class="promo-timer" data-end-time="${flower.endTime}">剩余 <span class="time-remaining">计算中...</span></div>
                </div>
            </a>
            <button class="btn btn-primary add-to-cart-btn" data-id="${flower.id}">
                <i class="fas fa-shopping-cart"></i> 加入购物车
            </button>
        `;
        promoContainer.appendChild(promoCard);
    });

    // 启动促销倒计时
    startPromoTimers();
}

/**
 * 启动促销倒计时
 */
function startPromoTimers() {
    const timerElements = document.querySelectorAll('.promo-timer');

    // 更新倒计时函数
    function updateTimers() {
        timerElements.forEach(timer => {
            const endTime = timer.dataset.endTime;
            const remaining = calculateTimeRemaining(endTime);

            if (remaining) {
                const { days, hours, minutes, seconds } = remaining;
                timer.querySelector('.time-remaining').textContent =
                    `${days > 0 ? days + '天 ' : ''}${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
            } else {
                timer.textContent = '活动已结束';
            }
        });
    }

    // 立即更新一次
    updateTimers();

    // 每秒更新一次
    setInterval(updateTimers, 1000);
}

/**
 * 加载热门推荐花卉
 */
function loadPopularFlowers() {
    // 获取热门花卉数据（实际应从API获取）
    const popularFlowers = [
        {
            id: 201,
            name: '19朵红玫瑰花束',
            image: 'static/images/popular1.jpg',
            price: 239,
            sales: 1258,
            tags: ['浪漫', '红玫瑰', '爱情']
        },
        {
            id: 202,
            name: '粉玫瑰礼盒',
            image: 'static/images/popular2.jpg',
            price: 298,
            sales: 986,
            tags: ['礼盒', '粉玫瑰', '纪念日']
        },
        {
            id: 203,
            name: '向日葵混合花束',
            image: 'static/images/popular3.jpg',
            price: 198,
            sales: 876,
            tags: ['向日葵', '混合', '生日']
        },
        {
            id: 204,
            name: '百合花束',
            image: 'static/images/popular4.jpg',
            price: 258,
            sales: 756,
            tags: ['百合', '清新', '祝福']
        }
    ];

    // 渲染热门花卉
    renderFlowerGrid(popularFlowers, 'popularFlowers');
}

/**
 * 加载新品上架花卉
 */
function loadNewFlowers() {
    // 获取新品花卉数据（实际应从API获取）
    const newFlowers = [
        {
            id: 301,
            name: '蓝色妖姬花束',
            image: 'static/images/new1.jpg',
            price: 269,
            sales: 128,
            tags: ['蓝玫瑰', '稀有', '高级']
        },
        {
            id: 302,
            name: '郁金香花盒',
            image: 'static/images/new2.jpg',
            price: 198,
            sales: 86,
            tags: ['郁金香', '花盒', '春季']
        },
        {
            id: 303,
            name: '多肉植物组合',
            image: 'static/images/new3.jpg',
            price: 158,
            sales: 156,
            tags: ['多肉', '绿植', '办公室']
        },
        {
            id: 304,
            name: '康乃馨礼篮',
            image: 'static/images/new4.jpg',
            price: 328,
            sales: 68,
            tags: ['康乃馨', '礼篮', '感恩']
        }
    ];

    // 渲染新品花卉
    renderFlowerGrid(newFlowers, 'newFlowers');
}

/**
 * 渲染花卉网格
 * @param {Array} flowers 花卉数据
 * @param {string} containerId 容器ID
 */
function renderFlowerGrid(flowers, containerId) {
    const container = document.getElementById(containerId);
    if (!container || !flowers.length) return;

    // 清空现有内容
    container.innerHTML = '';

    // 创建花卉卡片
    flowers.forEach(flower => {
        const flowerCard = document.createElement('div');
        flowerCard.className = 'flower-card';
        flowerCard.innerHTML = `
            <div class="flower-image">
                <a href="flower-detail.html?id=${flower.id}">
                    <img src="${flower.image}" alt="${flower.name}">
                </a>
                <div class="add-to-cart">
                    <button class="add-to-cart-btn" data-id="${flower.id}">加入购物车</button>
                </div>
            </div>
            <div class="flower-content">
                <h3 class="flower-title">
                    <a href="flower-detail.html?id=${flower.id}">${flower.name}</a>
                </h3>
                <div class="flower-price">${formatPrice(flower.price)}</div>
                <div class="flower-sales">已售 ${flower.sales} 件</div>
                <div class="flower-tags">
                    ${flower.tags.map(tag => `<span class="flower-tag">${tag}</span>`).join('')}
                </div>
            </div>
        `;
        container.appendChild(flowerCard);
    });
}

/**
 * 加载场景推荐
 */
function loadScenarios() {
    // 获取场景推荐数据（实际应从API获取）
    const scenarios = [
        {
            id: 1,
            title: '爱情表白',
            description: '用花语表达你的爱意',
            image: 'static/images/scenario1.jpg',
            link: 'flower-list.html?scenario=love'
        },
        {
            id: 2,
            title: '生日祝福',
            description: '为重要的日子增添惊喜',
            image: 'static/images/scenario2.jpg',
            link: 'flower-list.html?scenario=birthday'
        },
        {
            id: 3,
            title: '商务礼品',
            description: '专业得体的商务花礼',
            image: 'static/images/scenario3.jpg',
            link: 'flower-list.html?scenario=business'
        }
    ];

    // 渲染场景推荐
    renderScenarios(scenarios);
}

/**
 * 渲染场景推荐
 * @param {Array} scenarios 场景推荐数据
 */
function renderScenarios(scenarios) {
    const scenarioGrid = document.getElementById('scenarioGrid');
    if (!scenarioGrid || !scenarios.length) return;

    // 清空现有内容
    scenarioGrid.innerHTML = '';

    // 创建场景卡片
    scenarios.forEach(scenario => {
        const scenarioCard = document.createElement('div');
        scenarioCard.className = 'scenario-card';
        scenarioCard.innerHTML = `
            <a href="${scenario.link}">
                <img src="${scenario.image}" alt="${scenario.title}">
                <div class="scenario-overlay">
                    <h3 class="scenario-title">${scenario.title}</h3>
                    <p class="scenario-description">${scenario.description}</p>
                </div>
            </a>
        `;
        scenarioGrid.appendChild(scenarioCard);
    });
}

/**
 * 绑定加入购物车按钮事件
 */
function bindAddToCartButtons() {
    // 使用事件委托绑定所有加入购物车按钮
    document.body.addEventListener('click', function(e) {
        if (e.target.classList.contains('add-to-cart-btn') ||
            e.target.parentElement.classList.contains('add-to-cart-btn')) {

            // 阻止默认行为和事件冒泡
            e.preventDefault();
            e.stopPropagation();

            // 获取花卉ID
            const btn = e.target.classList.contains('add-to-cart-btn') ?
                  e.target : e.target.parentElement;
            const flowerId = btn.dataset.id;

            // 添加到购物车
            if (flowerId) {
                addToCart(parseInt(flowerId), 1);
            }
        }
    });
}