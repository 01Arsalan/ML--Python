# import asyncio
# import pandas as pd
# from playwright.async_api import async_playwright, TimeoutError, Error as PlaywrightError
# import os
# from urllib.parse import urlparse
# import re
# import logging
# import random
# import time
# from tqdm import tqdm 
# import json
# import aiohttp

# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# logger = logging.getLogger(__name__)

# async def wait_for_network_idle(page, timeout=30000):
#     try:
#         await page.wait_for_load_state('networkidle', timeout=timeout)
#     except TimeoutError:
#         logger.warning(f"Network idle timeout reached for {page.url}")

# async def bypass_cloudflare(page, url):
#     cloudflare_selector = "input[name='cf_captcha_kind']"
#     try:
#         await page.wait_for_selector(cloudflare_selector, timeout=5000)
#         logger.info(f"Cloudflare challenge detected for {url}")
#         # Wait for a longer period to potentially bypass the challenge
#         await asyncio.sleep(10)
#         await page.reload()
#         await wait_for_network_idle(page)
#     except TimeoutError:
#         # No Cloudflare challenge detected, continue normally
#         pass

# async def take_screenshot(page, id, url, output_dir, retry_count=0):
#     try:
#         logger.info(f"Processing {url} (ID: {id})")
#         await asyncio.sleep(random.uniform(1, 3))
        
#         user_agents = [
#             "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
#             "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15",
#             "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"
#         ]
#         chosen_ua = random.choice(user_agents)
#         await page.set_extra_http_headers({"User-Agent": chosen_ua})

#         try:
#             response = await asyncio.wait_for(page.goto(url, wait_until='domcontentloaded', timeout=60000), timeout=65.0)
#             if not response.ok:
#                 logger.warning(f"HTTP status {response.status} for {url} (ID: {id})")
#         except asyncio.TimeoutError:
#             logger.warning(f"Navigation timeout for {url}. Attempting to continue anyway.")

#         await bypass_cloudflare(page, url)
#         await wait_for_network_idle(page)

#         # Scroll to bottom and back to top to trigger lazy-loading
#         await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
#         await asyncio.sleep(2)
#         await page.evaluate("window.scrollTo(0, 0)")
#         await asyncio.sleep(2)

#         # Get the full page dimensions
#         dimensions = await page.evaluate('''() => {
#             return {
#                 width: document.documentElement.scrollWidth,
#                 height: document.documentElement.scrollHeight,
#             }
#         }''')

#         # Set the viewport to the full page size
#         await page.set_viewport_size(dimensions)

#         parsed_url = urlparse(url)
#         safe_name = re.sub(r'[^\w\-_\. ]', '_', parsed_url.netloc + parsed_url.path)
#         filename = f"{id}-{safe_name[:50]}.png"
#         filepath = os.path.join(output_dir, filename)
        
#         # Take a full page screenshot with progress
#         progress_bar = tqdm(total=100, desc=f"Capturing {filename}", unit="%")
#         await page.screenshot(path=filepath, full_page=True, timeout=120000)
#         progress_bar.close()
        
#         logger.info(f"Full page screenshot saved: {filepath}")
#         return True
#     except (TimeoutError, PlaywrightError) as e:
#         if retry_count < 2:
#             logger.warning(f"Error for {url} (ID: {id}): {str(e)}. Retrying... (Attempt {retry_count + 1})")
#             return await take_screenshot(page, id, url, output_dir, retry_count + 1)
#         else:
#             logger.error(f"Failed to process {url} (ID: {id}) after 3 attempts. Skipping.")
#             return False
#     except Exception as e:
#         logger.error(f"Error processing {url} (ID: {id}): {str(e)}")
#         return False

# async def check_url(session, url):
#     try:
#         async with session.head(url, allow_redirects=True, timeout=10) as response:
#             return response.status < 400
#     except:
#         return False

# async def process_urls(csv_path, output_dir, checkpoint_file):
#     start_time = time.time()
#     df = pd.read_csv(csv_path)
#     total_urls = len(df)
#     os.makedirs(output_dir, exist_ok=True)

#     logger.info(f"Checkpoint file location: {checkpoint_file}")

#     # Load checkpoint if it exists
#     start_index = 0
#     end_index = total_urls - 1
#     if os.path.exists(checkpoint_file):
#         with open(checkpoint_file, 'r') as f:
#             checkpoint = json.load(f)
#             start_index = checkpoint.get('last_processed_index', -1) + 1
#             end_index = checkpoint.get('end_index', total_urls - 1)
#         logger.info(f"Resuming from index {start_index}")
#         logger.info(f"Will process until index {end_index}")
#     else:
#         logger.info("Starting from the beginning (no checkpoint found)")
#         logger.info(f"Will process until index {end_index}")

#     async with async_playwright() as p:
#         browser = await p.chromium.launch(headless=True)
#         context = await browser.new_context()
        
#         page_pool = []
#         for _ in range(3):
#             page = await context.new_page()
#             page_pool.append(page)
        
#         progress_bar = tqdm(total=end_index-start_index+1, initial=0, desc="Processing URLs", unit="URL")
        
#         async with aiohttp.ClientSession() as session:
#             try:
#                 for index, row in df.iloc[start_index:end_index+1].iterrows():
#                     id = row['id']
#                     url = row['url']
#                     if pd.isna(url):
#                         logger.warning(f"Skipping empty URL for ID: {id}")
#                         progress_bar.update(1)
#                         continue
                    
#                     # Check if URL is accessible
#                     if not await check_url(session, url):
#                         logger.warning(f"URL not accessible: {url} (ID: {id}). Skipping.")
#                         progress_bar.update(1)
#                         continue
                    
#                     page = page_pool[index % len(page_pool)]
#                     try:
#                         success = await asyncio.wait_for(take_screenshot(page, id, url, output_dir), timeout=180.0)
#                     except asyncio.TimeoutError:
#                         logger.error(f"Total timeout for {url} (ID: {id}). Skipping.")
#                         success = False
                    
#                     progress_bar.update(1)
#                     progress_bar.set_postfix_str(f"Current: {url[:30]}...")
                    
#                     if success:
#                         logger.info(f"Successfully processed {url} (ID: {id})")
#                     else:
#                         logger.warning(f"Failed to process {url} (ID: {id})")
                    
#                     # Save checkpoint after each successful processing
#                     with open(checkpoint_file, 'w') as f:
#                         json.dump({'last_processed_index': index, 'end_index': end_index}, f)
                    
#                     await asyncio.sleep(random.uniform(1, 3))
                    
#                     elapsed_time = time.time() - start_time
#                     if elapsed_time > 1800:
#                         logger.warning("Process has been running for 30 minutes. Stopping.")
#                         break

#                     if index >= end_index:
#                         logger.info(f"Reached end index {end_index}. Stopping.")
#                         break

#             except Exception as e:
#                 logger.error(f"Unexpected error occurred: {str(e)}")
#             finally:
#                 progress_bar.close()
                
#                 for page in page_pool:
#                     await page.close()
                
#                 await browser.close()

#     total_time = time.time() - start_time
#     processed_urls = min(index - start_index + 1, end_index - start_index + 1)
#     logger.info(f"Process completed in {total_time:.2f} seconds")
#     logger.info(f"Processed {processed_urls} URLs")
#     logger.info(f"Average time per URL: {total_time / processed_urls:.2f} seconds")

# if __name__ == "__main__":
#     script_dir = os.path.dirname(os.path.abspath(__file__))
#     csv_path = os.path.join(script_dir, 'urls.csv')
#     output_dir = os.path.join(script_dir, 'screenshots')
#     checkpoint_file = os.path.join(script_dir, 'checkpoint.json')
    
#     logger.info(f"CSV file: {csv_path}")
#     logger.info(f"Output directory: {output_dir}")
#     logger.info(f"Checkpoint file: {checkpoint_file}")

#     asyncio.run(process_urls(csv_path, output_dir, checkpoint_file))




import asyncio
import pandas as pd
from playwright.async_api import async_playwright, TimeoutError, Error as PlaywrightError
import os
from urllib.parse import urlparse
import re
import logging
import random
import time
from tqdm import tqdm
import json
import aiohttp

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def wait_for_network_idle(page, timeout=30000):
    try:
        await page.wait_for_load_state('networkidle', timeout=timeout)
    except TimeoutError:
        logger.warning(f"Network idle timeout reached for {page.url}")

async def bypass_cloudflare(page, url):
    cloudflare_selector = "input[name='cf_captcha_kind']"
    try:
        await page.wait_for_selector(cloudflare_selector, timeout=5000)
        logger.info(f"Cloudflare challenge detected for {url}")
        await asyncio.sleep(10)
        await page.reload()
        await wait_for_network_idle(page)
    except TimeoutError:
        pass

async def remove_popup(page):
    techniques = [
        # Technique 1: Remove based on position and z-index
        '''() => {
            let popups = [...document.querySelectorAll('*')].filter(el => {
                const style = window.getComputedStyle(el);
                return (style.position === 'fixed' || style.position === 'absolute') && parseInt(style.zIndex) > 1000;
            });
            if (popups.length > 0) {
                popups.forEach(popup => popup.remove());
                return true;
            }
            return false;
        }''',

        # Technique 2: Remove based on element size
        '''() => {
            let popups = [...document.querySelectorAll('*')].filter(el => {
                const rect = el.getBoundingClientRect();
                return (rect.width > window.innerWidth * 0.5 || rect.height > window.innerHeight * 0.5) &&
                       rect.top >= 0 && rect.left >= 0;
            });
            if (popups.length > 0) {
                popups.forEach(popup => popup.remove());
                return true;
            }
            return false;
        }''',

        # Technique 3: Click close buttons by text (like "Close", "Dismiss", "X")
        '''() => {
            let closeButtons = [...document.querySelectorAll('button, div, span')].filter(el => {
                return /close|dismiss|x/i.test(el.innerText);
            });
            if (closeButtons.length > 0) {
                closeButtons.forEach(button => button.click());
                return true;
            }
            return false;
        }''',

        # Technique 4: Remove based on text content (like "Subscribe", "Offer", "Discount")
        '''() => {
            let popups = [...document.querySelectorAll('div, span, p')].filter(el => {
                return /subscribe|offer|discount|popup/i.test(el.innerText);
            });
            if (popups.length > 0) {
                popups.forEach(popup => popup.remove());
                return true;
            }
            return false;
        }''',

        # Technique 5: Handle popups inside iframes
        '''async () => {
            let iframeElement = document.querySelector('iframe');
            if (iframeElement) {
                let frame = iframeElement.contentWindow.document;
                let popups = [...frame.querySelectorAll('*')].filter(el => {
                    const style = window.getComputedStyle(el);
                    return (style.position === 'fixed' || style.position === 'absolute') && parseInt(style.zIndex) > 1000;
                });
                if (popups.length > 0) {
                    popups.forEach(popup => popup.remove());
                    return true;
                }
            }
            return false;
        }''',

        # Technique 6: Detect blocking modal elements based on viewport size
        '''() => {
            let blockingElements = [...document.querySelectorAll('*')].filter(el => {
                const rect = el.getBoundingClientRect();
                return rect.width >= window.innerWidth && rect.height >= window.innerHeight && 
                       el.style.pointerEvents === 'auto';
            });
            if (blockingElements.length > 0) {
                blockingElements.forEach(el => el.remove());
                return true;
            }
            return false;
        }''',

        # Technique 7: Use MutationObserver to catch dynamically added popups
        '''() => {
            const observer = new MutationObserver((mutations) => {
                for (let mutation of mutations) {
                    mutation.addedNodes.forEach(node => {
                        if (node.nodeType === 1) {
                            const style = window.getComputedStyle(node);
                            if ((style.position === 'fixed' || style.position === 'absolute') && parseInt(style.zIndex) > 1000) {
                                node.remove();
                            }
                        }
                    });
                }
            });
            observer.observe(document.body, { childList: true, subtree: true });
            return true;
        }''',

        # Technique 8: Final fallback - attempt to remove any remaining visible popups
        '''() => {
            let popups = [...document.querySelectorAll('*')].filter(el => {
                const style = window.getComputedStyle(el);
                return (style.position === 'fixed' || style.position === 'absolute');
            });
            if (popups.length > 0) {
                popups.forEach(popup => popup.remove());
                return true;
            }
            return false;
        }'''
    ]

    for technique in techniques:
        try:
            result = await page.evaluate(technique)
            if result:
                logger.info("Popup removed using one of the techniques.")
                return True
        except Exception as e:
            logger.debug(f"Error applying popup removal technique: {e}")

    return False


async def take_screenshot(page, id, url, output_dir, retry_count=0):
    try:
        logger.info(f"Processing {url} (ID: {id})")
        await asyncio.sleep(random.uniform(1, 3))

        # Set user agent
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"
        ]
        chosen_ua = random.choice(user_agents)
        await page.set_extra_http_headers({"User-Agent": chosen_ua})

        # Navigate to URL
        try:
            response = await asyncio.wait_for(page.goto(url, wait_until='domcontentloaded', timeout=60000), timeout=65.0)
            if not response.ok:
                logger.warning(f"HTTP status {response.status} for {url} (ID: {id})")
        except asyncio.TimeoutError:
            logger.warning(f"Navigation timeout for {url}. Attempting to continue anyway.")

        # Bypass Cloudflare and wait for network idle
        await bypass_cloudflare(page, url)
        await wait_for_network_idle(page)

        # Remove popups and ensure they are gone before continuing
        popups_removed = await remove_popup(page)
        if popups_removed:
            logger.info("Popups removed successfully.")
            # Ensure a small delay after removal to allow for UI changes to complete
            await asyncio.sleep(2)  # Optional, but helps ensure popups are gone
        else:
            logger.info("No popups detected or removed.")

        # Scroll to bottom and top to trigger lazy-loading
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await asyncio.sleep(2)
        await page.evaluate("window.scrollTo(0, 0)")
        await asyncio.sleep(2)

        # Adjust viewport size for the screenshot
        dimensions = await page.evaluate('''() => {
            return {
                width: Math.max(document.documentElement.scrollWidth, document.body.scrollWidth),
                height: Math.max(document.documentElement.scrollHeight, document.body.scrollHeight),
            }
        }''')
        await page.set_viewport_size({"width": dimensions['width'], "height": dimensions['height']})

        # Define output file path
        parsed_url = urlparse(url)
        safe_name = re.sub(r'[^\w\-_\. ]', '_', parsed_url.netloc + parsed_url.path)
        filename = f"{id}-{safe_name[:50]}.png"
        filepath = os.path.join(output_dir, filename)

        # Capture screenshot
        progress_bar = tqdm(total=100, desc=f"Capturing {filename}", unit="%")
        await page.screenshot(path=filepath, full_page=True, timeout=120000)
        progress_bar.close()

        logger.info(f"Full page screenshot saved: {filepath}")
        return True

    except (TimeoutError, PlaywrightError) as e:
        if retry_count < 2:
            logger.warning(f"Error for {url} (ID: {id}): {str(e)}. Retrying... (Attempt {retry_count + 1})")
            return await take_screenshot(page, id, url, output_dir, retry_count + 1)
        else:
            logger.error(f"Failed to process {url} (ID: {id}) after 3 attempts. Skipping.")
            return False
    except Exception as e:
        logger.error(f"Error processing {url} (ID: {id}): {str(e)}")
        return False


async def check_url(session, url):
    try:
        async with session.head(url, allow_redirects=True, timeout=10) as response:
            return response.status < 400
    except:
        return False

async def process_urls(csv_path, output_dir, checkpoint_file):
    start_time = time.time()
    df = pd.read_csv(csv_path)
    total_urls = len(df)
    os.makedirs(output_dir, exist_ok=True)

    logger.info(f"Checkpoint file location: {checkpoint_file}")

    # Load checkpoint if it exists
    start_index = 0
    end_index = total_urls - 1
    if os.path.exists(checkpoint_file):
        with open(checkpoint_file, 'r') as f:
            checkpoint = json.load(f)
            start_index = checkpoint.get('last_processed_index', -1) + 1
            end_index = checkpoint.get('end_index', total_urls - 1)
        logger.info(f"Resuming from index {start_index}")
        logger.info(f"Will process until index {end_index}")
    else:
        logger.info("Starting from the beginning (no checkpoint found)")
        logger.info(f"Will process until index {end_index}")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()

        page_pool = []
        for _ in range(3):
            page = await context.new_page()
            page_pool.append(page)

        progress_bar = tqdm(total=end_index-start_index+1, initial=0, desc="Processing URLs", unit="URL")

        async with aiohttp.ClientSession() as session:
            try:
                for index, row in df.iloc[start_index:end_index+1].iterrows():
                    id = row['id']
                    url = row['url']
                    if pd.isna(url):
                        logger.warning(f"Skipping empty URL for ID: {id}")
                        progress_bar.update(1)
                        continue

                    # Check if URL is accessible
                    if not await check_url(session, url):
                        logger.warning(f"URL not accessible: {url} (ID: {id}). Skipping.")
                        progress_bar.update(1)
                        continue

                    page = page_pool[index % len(page_pool)]
                    try:
                        success = await asyncio.wait_for(take_screenshot(page, id, url, output_dir), timeout=180.0)
                    except asyncio.TimeoutError:
                        logger.error(f"Total timeout for {url} (ID: {id}). Skipping.")
                        success = False

                    progress_bar.update(1)
                    progress_bar.set_postfix_str(f"Current: {url[:30]}...")

                    if success:
                        logger.info(f"Successfully processed {url} (ID: {id})")
                    else:
                        logger.warning(f"Failed to process {url} (ID: {id})")

                    # Save checkpoint after each successful processing
                    with open(checkpoint_file, 'w') as f:
                        json.dump({'last_processed_index': index, 'end_index': end_index}, f)

                    await asyncio.sleep(random.uniform(1, 3))

                    elapsed_time = time.time() - start_time
                    if elapsed_time > 1800:
                        logger.warning("Process has been running for 30 minutes. Stopping.")
                        break

                    if index >= end_index:
                        logger.info(f"Reached end index {end_index}. Stopping.")
                        break

            except Exception as e:
                logger.error(f"Unexpected error occurred: {str(e)}")
            finally:
                progress_bar.close()

                for page in page_pool:
                    await page.close()

                await browser.close()

    total_time = time.time() - start_time
    processed_urls = min(index - start_index + 1, end_index - start_index + 1)
    logger.info(f"Process completed in {total_time:.2f} seconds")
    logger.info(f"Processed {processed_urls} URLs")
    logger.info(f"Average time per URL: {total_time / processed_urls:.2f} seconds")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, 'lander_urls.csv')
    output_dir = os.path.join(script_dir, 'screenshots')
    checkpoint_file = os.path.join(script_dir, 'checkpoint.json')

    logger.info(f"CSV file: {csv_path}")
    logger.info(f"Output directory: {output_dir}")
    logger.info(f"Checkpoint file: {checkpoint_file}")

    asyncio.run(process_urls(csv_path, output_dir, checkpoint_file))