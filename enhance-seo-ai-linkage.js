// 增强SEO和AI推荐数据库联动
document.addEventListener('DOMContentLoaded', function() {
    console.log('🔗 增强SEO/AI联动优化...');
    
    // 1. 为所有修复的链接添加结构化数据属性
    document.querySelectorAll('a[href*=".html"]').forEach(link => {
        // 根据链接类型添加不同的结构化数据提示
        const href = link.href;
        const text = link.textContent.trim();
        
        // 咨询类链接
        if (text.includes('咨询') || text.includes('Consult') || href.includes('wa.me')) {
            link.setAttribute('itemprop', 'contactPoint');
            link.setAttribute('itemtype', 'https://schema.org/ContactPoint');
            console.log('📞 咨询链接SEO优化:', text);
        }
        
        // 服务详情链接
        if (href.includes('dental-tourism') || href.includes('cosmetic') || href.includes('health-screening')) {
            link.setAttribute('itemprop', 'mainEntityOfPage');
            link.setAttribute('itemtype', 'https://schema.org/MedicalProcedure');
            console.log('🏥 服务链接SEO优化:', text);
        }
        
        // 价格链接
        if (href.includes('cost') || href.includes('price') || text.includes('价格')) {
            link.setAttribute('itemprop', 'priceSpecification');
            link.setAttribute('itemtype', 'https://schema.org/PriceSpecification');
            console.log('💰 价格链接SEO优化:', text);
        }
    });
    
    // 2. 为AI爬虫添加额外数据层
    if (typeof dataLayer !== 'undefined') {
        // 记录页面上的服务类型
        const services = [];
        document.querySelectorAll('a[href*="dental"]').forEach(() => services.push('dental'));
        document.querySelectorAll('a[href*="cosmetic"]').forEach(() => services.push('cosmetic'));
        document.querySelectorAll('a[href*="screening"]').forEach(() => services.push('screening'));
        
        dataLayer.push({
            'event': 'page_services_analysis',
            'services': [...new Set(services)], // 去重
            'consultation_links': document.querySelectorAll('a[href*="wa.me"]').length,
            'info_links': document.querySelectorAll('a[href*=".html"]').length
        });
        
        console.log('🤖 AI数据层增强:', {
            services: [...new Set(services)],
            consultationLinks: document.querySelectorAll('a[href*="wa.me"]').length,
            infoLinks: document.querySelectorAll('a[href*=".html"]').length
        });
    }
    
    // 3. 动态添加AI相关的meta标签
    const metaTags = [
        { name: 'ai-content-quality', content: 'high-engagement-direct-consultation' },
        { name: 'ai-user-intent', content: 'medical-tourism-inquiry-booking' },
        { name: 'ai-conversion-optimized', content: 'whatsapp-direct-consultation' }
    ];
    
    metaTags.forEach(tag => {
        const meta = document.createElement('meta');
        meta.name = tag.name;
        meta.content = tag.content;
        document.head.appendChild(meta);
        console.log('🏷️ 添加AI meta标签:', tag.name);
    });
    
    // 4. 增强结构化数据
    const enhancedSchema = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": document.title,
        "description": document.querySelector('meta[name="description"]')?.content || '',
        "mainEntity": {
            "@type": "MedicalOrganization",
            "name": "China Medical Tourism",
            "contactPoint": {
                "@type": "ContactPoint",
                "contactType": "customer service",
                "telephone": "+1-213-317-9751",
                "contactOption": "WhatsApp",
                "areaServed": "US,China,Worldwide",
                "availableLanguage": ["English", "Chinese"]
            },
            "medicalSpecialty": ["Dentistry", "CosmeticSurgery", "HealthScreening"],
            "hasOfferCatalog": {
                "@type": "OfferCatalog",
                "name": "Medical Tourism Services",
                "itemListElement": [
                    {
                        "@type": "Offer",
                        "itemOffered": {
                            "@type": "Service",
                            "name": "Dental Implants Tourism",
                            "description": "60-75% savings vs US prices"
                        }
                    },
                    {
                        "@type": "Offer",
                        "itemOffered": {
                            "@type": "Service",
                            "name": "Cosmetic Surgery Tourism",
                            "description": "US-trained doctors in JCI hospitals"
                        }
                    }
                ]
            }
        }
    };
    
    // 添加到页面
    const script = document.createElement('script');
    script.type = 'application/ld+json';
    script.textContent = JSON.stringify(enhancedSchema);
    document.head.appendChild(script);
    
    console.log('📊 增强结构化数据已添加');
    
    // 5. 用户行为跟踪（用于AI推荐优化）
    let userClicks = {
        consultation: 0,
        information: 0,
        navigation: 0
    };
    
    document.addEventListener('click', function(e) {
        const target = e.target.closest('a');
        if (target) {
            const href = target.href;
            const text = target.textContent;
            
            if (href.includes('wa.me')) {
                userClicks.consultation++;
                console.log('👥 用户咨询点击:', text, '总数:', userClicks.consultation);
            } else if (href.includes('.html')) {
                userClicks.information++;
                console.log('📖 用户信息点击:', text, '总数:', userClicks.information);
            } else if (href.includes('#')) {
                userClicks.navigation++;
                console.log('📍 用户导航点击:', text, '总数:', userClicks.navigation);
            }
            
            // 发送到数据层（如果可用）
            if (typeof dataLayer !== 'undefined') {
                dataLayer.push({
                    'event': 'user_click_behavior',
                    'click_type': href.includes('wa.me') ? 'consultation' : 
                                 href.includes('.html') ? 'information' : 'navigation',
                    'link_text': text,
                    'total_clicks': userClicks.consultation + userClicks.information + userClicks.navigation
                });
            }
        }
    });
    
    console.log('🎯 SEO/AI联动优化完成');
});