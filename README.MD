# ice-breaking

Welcome to the `ice-breaking` repository! Below are the detailed steps and instructions on how to use the scripts and tools provided in this repository.

## Data Privacy

The data in the `data` directory has been anonymized to remove personal user information. For more details on the anonymization process, please refer to `ethic_clean.py`.

## Prerequisites

Before running the scripts, you need to download the appropriate version of the `chromedriver` for your operating system:
- **Windows:** Download `chromedriver-win64`
- **Mac:** Download the corresponding version of `chromedriver` for Mac

Make sure to modify the path in the script accordingly:
```python
path = 'D:/chromedriver-win64/chromedriver.exe'
```
When you run the script, a login screen will appear. Please log in via Weibo's QR code scanner. (Due to the complexity of Weibo's login verification, fully automated user ID retrieval is not possible.)

## Steps to Follow

### 1. Retrieve User IDs from the Depression Super-Topic

Run the following command to get user IDs:
```bash
python get-user-id.py
```
The retrieved IDs will be stored in `data/depressed_ids.txt`.

### 2. Depression User Classification

Navigate to the `TextClassify_with_BERT-master` folder. You may need to retrain the depression user classifier using the user's posting history data. The input for the classifier should be a combination of the user's historical posts, current posts, and comments to strangers.

### 3. Crawl User Information and Posts

To crawl user information and posts based on the IDs in `depressed_ids.txt`, navigate to the `weibo-user-crawler` folder. You can modify `config.json` according to your needs, focusing on the following three parameters:
```json
"user_id_list": "depression_ids.txt",
"since_date": 90,
"write_mode": ["csv"]
```
For more details, refer to the `README.md` in the `weibo-user-crawler` folder. Run the following command:
```bash
nohup python -u weibo.py > result.log 2>&1 &
```
This will generate a `weibo` folder containing `users.csv` (which stores user information) and CSV files for each user's posts and comments.

### 4. Identify Ice-Breaking Posts

Run the following command to identify ice-breaking posts:
```bash
python best-icebk-point.py
```
The script will traverse the `data/weibo` folder (make sure to move `users.csv` out) and classify posts into positive and negative based on the criteria mentioned in the related paper. Positive posts are those that need ice-breaking.

### 5. Generate Icebreakers

Navigate to the `reply` folder for detailed usage instructions in its `README.md`. The folder contains four prompt strategies:
- `reply_by_chat1`
- `reply_by_chat2`
- `reply_by_chat3`
- `reply_by_chat4`

### 6. Multi-Label Classification of Post and Reply Types

Navigate to the `multi_label` folder for multi-label classification of post types and reply types.

## Contact

For any questions or issues, please open an issue on this repository or contact the maintainers.

---

Thank you for using `ice-breaking`! We hope this helps you in your research and interactions on Weibo.
