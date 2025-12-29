using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Audio;
using UnityEngine.UI;
using System.Linq;
using TMPro;

public class Options : MonoBehaviour
{
    public AudioMixer masterAudio;
    public TMP_Dropdown resDropdown;
    public Toggle fullScreenToggle;

    List<Resolution> proc_resolutions = new List<Resolution>();

    private void Start()
    {
        Resolution[] raw_resolutions = Screen.resolutions;
        List<int[]> resolutions = new List<int[]>();
        List<List<double>> refreshRates = new List<List<double>>();
        List<string> resText = new List<string>();


        resDropdown.ClearOptions();

        int currentResIndex = 0;
        for (int i = 0; i < raw_resolutions.Length; i++)
        {
            int[] raw_res = new int[] { raw_resolutions[i].width, raw_resolutions[i].height };

            // Verify the dimensions with existing resolutions
            bool match = false;
            for (int j = 0; j < resolutions.Count; j++)
            {
                // Match
                if (resolutions[j][0] == raw_res[0] && resolutions[j][1] == raw_res[1])
                {
                    refreshRates[j].Add(raw_resolutions[i].refreshRateRatio.value);
                    match = true;
                    break;
                }
            }
            if (match)
            {
                continue;
            }
            // No Match
            resolutions.Add(raw_res);
            proc_resolutions.Add(raw_resolutions[i]);
            refreshRates.Add(new List<double> { raw_resolutions[i].refreshRateRatio.value });
            string option = raw_res[0] + " x " + raw_res[1];
            resText.Add(option);
            if (raw_res[0] == Screen.currentResolution.width &&
            raw_res[1] == Screen.currentResolution.height)
            {
                currentResIndex = resText.Count - 1;
            }

        }

        resDropdown.AddOptions(resText);
        resDropdown.value = currentResIndex;
        resDropdown.RefreshShownValue();
        fullScreenToggle.isOn = Screen.fullScreen;

    }

    public void SetVolume(float volume)
    {
        masterAudio.SetFloat("volume", volume);
    }

    public void SetQuality(int qualityIndex)
    {
        QualitySettings.SetQualityLevel(qualityIndex);
    }

    public void SetFullScreen(bool isFullScreen)
    {
        Screen.fullScreen = isFullScreen;
    }

    public void SetResolution(int resolutionIndex)
    {
        Resolution res = proc_resolutions[resolutionIndex];
        Screen.SetResolution(res.width, res.height, Screen.fullScreen);
    }
}