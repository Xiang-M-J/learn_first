import os
import re
import shutil

# Markdown image regex: ![alt](path)
IMAGE_PATTERN = re.compile(r'!\[[^\]]*\]\(([^)]+)\)')

def process_markdown_images(folder_path):
    folder_path = os.path.abspath(folder_path)
    images_dir = os.path.join(folder_path, "images")

    if not os.path.exists(images_dir):
        os.makedirs(images_dir)

    # Traverse all md files
    for filename in os.listdir(folder_path):
        if filename.endswith(".md"):
            md_name = os.path.splitext(os.path.basename(filename))[0]
            md_path = os.path.join(folder_path, filename)

            with open(md_path, "r", encoding="utf-8") as f:
                content = f.read()

            updated_content = content
            modified = False
            
            # Find image links
            matches = IMAGE_PATTERN.findall(content)
            for img_path in matches:
                original_img_path = img_path

                # Remove surrounding quotes if exist
                img_path: str = img_path.strip('"').strip("'")

                if img_path.startswith("http") or img_path.startswith("https"):
                    continue

                # If absolute path or has folder structure, normalize
                abs_img_path = img_path
                if not os.path.isabs(img_path):
                    abs_img_path = os.path.abspath(os.path.join(folder_path, img_path))

                if not os.path.exists(abs_img_path):
                    print(f"[警告] 找不到图片：{img_path}，跳过")
                    continue

                # If the image is already in folder but not in images/
                if folder_path in os.path.dirname(abs_img_path):
                    # Modify to relative path (./name)
                    new_relative_path = os.path.relpath(abs_img_path, folder_path)
                    if original_img_path != new_relative_path:
                        updated_content = updated_content.replace(original_img_path, new_relative_path)
                        modified = True
                else:
                    # Copy file to images/
                    target_dir = os.path.join(images_dir, md_name)
                    if not os.path.exists(target_dir): os.makedirs(target_dir)
                    target_path = os.path.join(target_dir, os.path.basename(abs_img_path))
                    shutil.copy2(abs_img_path, target_path)
                    print(f"[复制] {abs_img_path} → {target_path}")

                    new_relative_path = os.path.join("images", md_name, os.path.basename(abs_img_path))
                    updated_content = updated_content.replace(original_img_path, new_relative_path)
                    modified = True

            # Rewrite markdown if modified
            if modified:
                with open(md_path, "w", encoding="utf-8") as f:
                    f.write(updated_content)
                print(f"[更新] 已更新图片路径：{md_path}")

    print("\n处理完成 ✔️")

if __name__ == "__main__":
    process_markdown_images("./")
