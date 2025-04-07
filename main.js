// AI Governance Digital Garden
// JavaScript for tag filtering and interactive elements

document.addEventListener('DOMContentLoaded', function() {
  // Tag filtering functionality
  setupTagFiltering();
  
  // Highlight toggling
  setupHighlightToggle();
  
  // Mobile navigation toggle
  setupMobileNav();
});

/**
 * Sets up tag filtering functionality
 */
function setupTagFiltering() {
  const tagLinks = document.querySelectorAll('.tag');
  const articles = document.querySelectorAll('.article');
  const activeTagsContainer = document.getElementById('active-tags');
  let activeTags = new Set();
  
  // Add click event to each tag
  tagLinks.forEach(tag => {
    tag.addEventListener('click', function(e) {
      e.preventDefault();
      
      const tagValue = this.getAttribute('data-tag');
      
      // Toggle tag active state
      if (activeTags.has(tagValue)) {
        activeTags.delete(tagValue);
        this.classList.remove('active');
      } else {
        activeTags.add(tagValue);
        this.classList.add('active');
      }
      
      // Update active tags display
      updateActiveTagsDisplay(activeTags);
      
      // Filter articles based on active tags
      filterArticles(activeTags);
    });
  });
  
  /**
   * Updates the display of active tags
   */
  function updateActiveTagsDisplay(tags) {
    // Clear current active tags
    activeTagsContainer.innerHTML = '';
    
    if (tags.size === 0) {
      // If no active tags, hide the container
      activeTagsContainer.style.display = 'none';
      return;
    }
    
    // Show the container
    activeTagsContainer.style.display = 'block';
    
    // Add each active tag with a remove button
    tags.forEach(tag => {
      const tagElement = document.createElement('span');
      tagElement.classList.add('active-tag');
      tagElement.innerHTML = `${tag} <button class="remove-tag" data-tag="${tag}">×</button>`;
      activeTagsContainer.appendChild(tagElement);
    });
    
    // Add event listeners to remove buttons
    document.querySelectorAll('.remove-tag').forEach(button => {
      button.addEventListener('click', function() {
        const tagToRemove = this.getAttribute('data-tag');
        activeTags.delete(tagToRemove);
        
        // Update tag links to reflect removed tag
        document.querySelector(`.tag[data-tag="${tagToRemove}"]`).classList.remove('active');
        
        // Update display and filter
        updateActiveTagsDisplay(activeTags);
        filterArticles(activeTags);
      });
    });
  }
  
  /**
   * Filters articles based on active tags
   */
  function filterArticles(tags) {
    if (tags.size === 0) {
      // If no tags are active, show all articles
      articles.forEach(article => {
        article.style.display = 'block';
      });
      return;
    }
    
    // Check each article against active tags
    articles.forEach(article => {
      const articleTags = article.getAttribute('data-tags').split(',');
      
      // Check if article has at least one active tag
      const hasActiveTag = Array.from(tags).some(tag => articleTags.includes(tag));
      
      // Show or hide based on tag match
      article.style.display = hasActiveTag ? 'block' : 'none';
    });
  }
}

/**
 * Sets up highlight toggling functionality
 */
function setupHighlightToggle() {
  const highlightToggle = document.getElementById('highlight-toggle');
  
  if (highlightToggle) {
    highlightToggle.addEventListener('change', function() {
      const highlights = document.querySelectorAll('.highlight');
      
      if (this.checked) {
        // Enable highlights
        highlights.forEach(highlight => {
          highlight.style.backgroundColor = 'var(--highlight-color)';
        });
      } else {
        // Disable highlights
        highlights.forEach(highlight => {
          highlight.style.backgroundColor = 'transparent';
        });
      }
    });
  }
}

/**
 * Sets up mobile navigation toggle
 */
function setupMobileNav() {
  const menuToggle = document.getElementById('menu-toggle');
  const mobileNav = document.getElementById('mobile-nav');
  
  if (menuToggle && mobileNav) {
    menuToggle.addEventListener('click', function() {
      mobileNav.classList.toggle('active');
      this.setAttribute('aria-expanded', 
        this.getAttribute('aria-expanded') === 'true' ? 'false' : 'true'
      );
    });
  }
}

/**
 * Language detection and translation support
 * (Placeholder for future implementation)
 */
function detectLanguage() {
  const userLang = navigator.language || navigator.userLanguage;
  return userLang.split('-')[0]; // Get primary language code
}

/**
 * Search functionality
 */
function setupSearch() {
  const searchInput = document.getElementById('search-input');
  const searchResults = document.getElementById('search-results');
  
  if (searchInput && searchResults) {
    searchInput.addEventListener('input', function() {
      const query = this.value.toLowerCase();
      
      if (query.length < 2) {
        searchResults.innerHTML = '';
        return;
      }
      
      // Get all articles
      const articles = document.querySelectorAll('.article');
      let results = [];
      
      // Search through articles
      articles.forEach(article => {
        const title = article.querySelector('.article-title').textContent.toLowerCase();
        const excerpt = article.querySelector('.article-excerpt').textContent.toLowerCase();
        
        if (title.includes(query) || excerpt.includes(query)) {
          results.push({
            title: article.querySelector('.article-title').textContent,
            url: article.querySelector('.article-title a').getAttribute('href')
          });
        }
      });
      
      // Display results
      displaySearchResults(results);
    });
    
    function displaySearchResults(results) {
      searchResults.innerHTML = '';
      
      if (results.length === 0) {
        searchResults.innerHTML = '<p>No results found</p>';
        return;
      }
      
      const resultsList = document.createElement('ul');
      
      results.forEach(result => {
        const listItem = document.createElement('li');
        listItem.innerHTML = `<a href="${result.url}">${result.title}</a>`;
        resultsList.appendChild(listItem);
      });
      
      searchResults.appendChild(resultsList);
    }
  }
}
