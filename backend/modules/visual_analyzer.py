"""
Module 2: Visual Analyzer
Analyzes webpage screenshots for phishing indicators using CLIP AI.
"""

from PIL import Image
import torch
from transformers import CLIPProcessor, CLIPModel
import numpy as np

class VisualAnalyzer:
    """Analyzes webpage screenshots using CLIP vision-language AI."""

    def __init__(self):
        """Initialize the visual analyzer with CLIP model."""
        print("Loading CLIP model... (first time takes 1-2 minutes)")

        # Load CLIP model and processor
        self.model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
        self.processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

        # Set to evaluation mode
        self.model.eval()

        # Define text prompts for classification
        self.prompts = {
            'legitimate': [
                "a legitimate professional website",
                "an official company homepage",
                "a secure banking website",
                "a trustworthy e-commerce site"
            ],
            'phishing': [
                "a fake phishing webpage",
                "a fraudulent login page",
                "a scam website trying to steal credentials",
                "a suspicious fake banking page"
            ],
            'suspicious_elements': [
                "urgent warning messages",
                "account suspended alert",
                "verify your account now",
                "click here immediately",
                "poor quality design",
                "suspicious login form"
            ]
        }

        # Known legitimate brand keywords
        self.legitimate_brands = [
            'PayPal', 'Amazon', 'Google', 'Microsoft', 'Apple',
            'Facebook', 'Netflix', 'Instagram', 'Twitter', 'LinkedIn',
            'Bank of America', 'Chase', 'Wells Fargo'
        ]

        print("✅ CLIP model loaded successfully!")

    def analyze(self, image_input):
        """
        Analyze a screenshot for phishing indicators.

        Args:
            image_input: Can be:
                - PIL Image object
                - File path (str)
                - NumPy array

        Returns:
            dict: Analysis results with risk score and details
        """
        try:
            # Load and preprocess image
            image = self._load_image(image_input)

            if image is None:
                return self._error_result("Failed to load image")

            # Initialize results
            risk_score = 0
            flags = []

            # Analysis 1: Legitimate vs Phishing classification
            legit_score, phish_score = self._classify_legitimacy(image)

            if phish_score > legit_score:
                risk_score += 40
                flags.append(f"⚠️ Image appears suspicious (phishing confidence: {phish_score:.1%})")
            elif phish_score > 0.3:
                risk_score += 20
                flags.append(f"⚠️ Some phishing indicators detected ({phish_score:.1%})")
            else:
                flags.append(f"✅ Image appears legitimate ({legit_score:.1%} confidence)")

            # Analysis 2: Check for suspicious visual elements
            suspicious_elements = self._detect_suspicious_elements(image)

            if len(suspicious_elements) > 0:
                risk_score += min(30, len(suspicious_elements) * 10)
                top_elements = suspicious_elements[:3]
                flags.append(f"⚠️ Suspicious visual elements: {', '.join(top_elements)}")

            # Analysis 3: Image quality check (phishing sites often have poor quality)
            quality_score = self._check_image_quality(image)

            if quality_score < 0.4:
                risk_score += 15
                flags.append(f"⚠️ Low image quality (often seen in phishing pages)")

            # Analysis 4: Color scheme analysis
            color_risk = self._analyze_colors(image)

            if color_risk > 0:
                risk_score += color_risk
                if color_risk > 10:
                    flags.append("⚠️ Unusual color scheme for legitimate sites")

            # Cap risk score at 100
            risk_score = min(100, risk_score)

            # Determine verdict
            if risk_score >= 70:
                verdict = "PHISHING"
                verdict_color = "🔴"
            elif risk_score >= 40:
                verdict = "SUSPICIOUS"
                verdict_color = "🟡"
            else:
                verdict = "SAFE"
                verdict_color = "🟢"

            return {
                'risk_score': risk_score,
                'verdict': verdict,
                'verdict_color': verdict_color,
                'flags': flags,
                'details': {
                    'legitimate_score': float(legit_score),
                    'phishing_score': float(phish_score),
                    'quality_score': float(quality_score),
                    'suspicious_elements': suspicious_elements,
                    'image_size': image.size
                }
            }

        except Exception as e:
            return self._error_result(f"Error during analysis: {str(e)}")

    def _load_image(self, image_input):
        """Load image from various input types."""
        try:
            if isinstance(image_input, str):
                # File path
                return Image.open(image_input).convert('RGB')
            elif isinstance(image_input, Image.Image):
                # PIL Image
                return image_input.convert('RGB')
            elif isinstance(image_input, np.ndarray):
                # NumPy array
                return Image.fromarray(image_input).convert('RGB')
            else:
                return None
        except Exception as e:
            print(f"Error loading image: {e}")
            return None

    def _classify_legitimacy(self, image):
        """
        Use CLIP to classify if image is legitimate or phishing.

        Returns:
            tuple: (legitimate_score, phishing_score)
        """
        try:
            # Combine all prompts
            all_prompts = self.prompts['legitimate'] + self.prompts['phishing']

            # Process image and text
            inputs = self.processor(
                text=all_prompts,
                images=image,
                return_tensors="pt",
                padding=True
            )

            # Get predictions
            with torch.no_grad():
                outputs = self.model(**inputs)
                logits_per_image = outputs.logits_per_image
                probs = logits_per_image.softmax(dim=1).squeeze()

            # Calculate average scores
            num_legit = len(self.prompts['legitimate'])
            legit_score = probs[:num_legit].mean().item()
            phish_score = probs[num_legit:].mean().item()

            return legit_score, phish_score

        except Exception as e:
            print(f"Error in classification: {e}")
            return 0.5, 0.5  # Neutral scores on error

    def _detect_suspicious_elements(self, image):
        """
        Detect suspicious visual elements using CLIP.

        Returns:
            list: List of detected suspicious elements
        """
        try:
            suspicious = []

            # Process image with suspicious element prompts
            inputs = self.processor(
                text=self.prompts['suspicious_elements'],
                images=image,
                return_tensors="pt",
                padding=True
            )

            # Get predictions
            with torch.no_grad():
                outputs = self.model(**inputs)
                logits_per_image = outputs.logits_per_image
                probs = logits_per_image.softmax(dim=1).squeeze()

            # Elements with score > 0.25 are considered detected
            threshold = 0.25
            for i, element in enumerate(self.prompts['suspicious_elements']):
                if probs[i].item() > threshold:
                    suspicious.append(element)

            return suspicious

        except Exception as e:
            print(f"Error detecting elements: {e}")
            return []

    def _check_image_quality(self, image):
        """
        Check image quality (phishing sites often have poor quality screenshots).

        Returns:
            float: Quality score (0-1, higher is better)
        """
        try:
            # Convert to numpy array
            img_array = np.array(image)

            # Calculate variance (higher variance = better quality)
            variance = np.var(img_array) / 10000.0
            variance = min(variance, 1.0)

            # Check resolution
            width, height = image.size
            total_pixels = width * height

            # Good quality if > 300x300
            resolution_score = min(total_pixels / (300 * 300), 1.0)

            # Combined quality score
            quality = (variance * 0.6) + (resolution_score * 0.4)

            return quality

        except Exception as e:
            print(f"Error checking quality: {e}")
            return 0.5

    def _analyze_colors(self, image):
        """
        Analyze color scheme for suspicious patterns.

        Returns:
            int: Risk score contribution (0-20)
        """
        try:
            # Resize for faster processing
            img_small = image.resize((100, 100))
            img_array = np.array(img_small)

            # Calculate dominant colors
            avg_color = img_array.mean(axis=(0, 1))

            # Check for unusual color schemes
            risk = 0

            # Very bright red (common in phishing alerts)
            if avg_color[0] > 200 and avg_color[1] < 100 and avg_color[2] < 100:
                risk += 15

            # Very dark overall (suspicious)
            if avg_color.mean() < 50:
                risk += 10

            # Very bright/washed out (poor quality)
            if avg_color.mean() > 230:
                risk += 10

            return risk

        except Exception as e:
            print(f"Error analyzing colors: {e}")
            return 0

    def _error_result(self, error_message):
        """Return error result format."""
        return {
            'risk_score': 50,
            'verdict': 'ERROR',
            'verdict_color': '⚠️',
            'flags': [f'⚠️ {error_message}'],
            'details': {'error': error_message}
        }


# Test function
def test_visual_analyzer():
    """Test the visual analyzer."""
    print("=" * 80)
    print("VISUAL ANALYZER TEST")
    print("=" * 80)

    # Initialize analyzer (downloads model first time)
    analyzer = VisualAnalyzer()

    # Create test images (since we don't have real screenshots yet)
    print("\nℹ️  Creating test images (placeholder)")
    print("In real use, you would pass actual screenshot images")

    # Create a simple test image
    test_img = Image.new('RGB', (800, 600), color=(255, 255, 255))

    print("\nAnalyzing test image...")
    result = analyzer.analyze(test_img)

    print(f"\nVerdict: {result['verdict_color']} {result['verdict']}")
    print(f"Risk Score: {result['risk_score']}%")
    print("\nFlags:")
    for flag in result['flags']:
        print(f"  {flag}")

    print("\nDetails:")
    for key, value in result['details'].items():
        if isinstance(value, float):
            print(f"  {key}: {value:.2f}")
        else:
            print(f"  {key}: {value}")

    print("\n" + "=" * 80)
    print("✅ Visual Analyzer is working!")
    print("Note: First run downloads CLIP model (~350MB)")
    print("=" * 80)


if __name__ == "__main__":
    # Run test when this file is executed directly
    test_visual_analyzer()
