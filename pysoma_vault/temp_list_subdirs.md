
#data
---
```yaml
# project dirs
None:
  post_app_subdir_data: &post_app_subdir_data
    - fusion_dir:
      - name: Fusion
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children:
    - nuke_dir:
      - name: Nuke
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children:
    - resolve_dir:
      - name: Resolve
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children:
    - adobe_dir:
      - name: Adobe
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children:
  tex_app_subdir_data: &tex_app_subdir_data
    - affinity_dir:
      - name: Affinity
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children:
    - adobe_dir:
      - name: Adobe
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children:
    - krita_dir:
      - name: krita
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children:
    - gimp_dir:
      - name: Gimp
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children:
    - substance_dir:
      - name: Substance
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children:
    - other_dir:
      - name: Other
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children:
  audio_app_subdir_data: &audio_app_subdir_data
    - pro_tools_dir:
      - name: Pro_Tools
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children:
    - ableton_dir:
      - name: Ableton
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children:
    - bitwig_dir:
      - name: Bitwig
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children:
    - reaper_dir:
      - name: Reaper
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children:
    - reason_dir:
      - name: Reason
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children:
    - other_dir:
      - name: Other
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children:
  comp_app_subdir_data: &comp_app_subdir_data
    - fusion_dir:
      - name: Fusion
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children:
    - resolve_dir:
      - name: Resolve
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children:
    - nuke_dir:
      - name: Nuke
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children:
    - adobe_dir:
      - name: Adobe
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children:
    - other_dir:
      - name: Other
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children:
  edit_app_data: &edit_app_data
    - resolve_dir:
      - name: resolve
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children:
    - adobe_dir:
      - name: adobe
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children:
  audio_subdir_data: &audio_subdir_data
    - sfx_dir:
      - name: SFX
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children:
    - music_dir:
      - name: Music
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children:
    - reference_dir:
      - name: reference
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children:
    - project_files_dir:
      - name: SFX
      - type: directory
      - path:
      - env:
      - h_env:
      - files: README.md
      - gitkeep: True
      - parent:
      - children: *audio_app_subdir_data
    - other_dir:
      - name: Other
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children:
  post_tex_subdir_data: &post_tex_subdir_data
    - data_tex_dir:
      - name: Data_Textures
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children:
    - alphas_dir:
      - name: Alphas
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children:
    - masks_dir:
      - name: Masks
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children:
    - pbr_dir:
      - name: PBR
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children:
    - pbr_dir:
      - name: PBR
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children:
    - grunge_dir:
      - name: Grunge
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children:
    - substance_dir:
      - name: Substance
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children:
      - sbr_dir:
        - name: sbr
        - type: directory
        - path:
        - env:
        - h_env:
        - files:
        - gitkeep: True
        - parent:
        - children:
    - project_files_dir:
      - name: Project_Files
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children: *post_app_subdir_data
    - other_dir:
      - name: Other
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children:
  src_subdir_data: &src_subdir_data
    - blender_dir:
      - name: Blender
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children:
    - maya_dir:
      - name: Maya
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children:
    - zbrush_dir:
      - name: ZBrush
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children:
    - substance_dir:
      - name: Substance
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children:
    - other_dir:
      - name: Other
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children:
  geo_subdir_data: &geo_subdir_data
    - fbx_dir:
      - name: FBX
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children:
    - obj_dir:
      - name: OBJ
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children:
    - houdini_dir:
      - name: Houdini
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children:
    - usd_dir:
      - name: USD
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children:
    - cache_dir:
      - name: cache
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children:
    - other_dir:
      - name: Other
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children:
  tex_subdir_data: &tex_subdir_data
    - hdri_dir:
      - name: HDRI
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children:
    - imperfections_dir:
      - name: Imperfections
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children:
    - pbr_dir:
      - name: PBR
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children:
    - data_tex_dir:
      - name: Data_Textures
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children:
    - decals_dir:
      - name: Decals
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children:
    - substance_dir:
      - name: Substance
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children:
    - alphas_dir:
      - name: Alphas
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children:
    - masks_dir:
      - name: Masks
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children:
    - grunge_dir:
      - name: Grunge
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children:
    - other_dir:
      - name: Other
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children:
  assets_subdir_data: &assets_subdir_data
    - src_dir:
      - name: SRC
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children:
    - geo_dir:
      - name: GEO
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children:
    - blend_dir:
      - name: Blend
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children:
    - texture_dir:
      - name: Texture
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children:
    - hda_dir:
      - name: HDA
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children:
    - other_dir:
      - name: Other
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children:
    - pdg_dir:
      - name: PDG
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children:
    - usd_dir:
      - name: USD
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children:
  comp_subdir_data: &comp_subdir_data
    - luts_dir:
      - name: LUTS
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children:
    - color_scripts_dir:
      - name: Color_Scripts
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children:
    - project_files_dir:
      - name: Project_Files
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children:
    - other_dir:
      - name: Other
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children:
    - export_dir:
      - name: export
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children:
  edit_subdir_data: &edit_subdir_data
    - project_files_dir:
      - name: Project_Files
      - type: directory
      - path:
      - env:
      - h_env:
      - files: README.md
      - gitkeep: True
      - parent:
      - children: *edit_app_data
    - export_dir:
      - name: export
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children:
  post_pro_subdir_data: &post_pro_subdir_data
    - audio_dir:
      - name: Audio
      - type: directory
      - path:
      - env:
      - h_env:
      - files: README.md
      - gitkeep: True
      - parent:
      - children: *audio_subdir_data
    - comp_dir:
      - name: Compositing
      - type: directory
      - path:
      - env:
      - h_env:
      - files: README.md
      - gitkeep: True
      - parent:
      - children: *comp_subdir_data
    - editing_dir:
      - name: Editing
      - type: directory
      - path:
      - env:
      - h_env:
      - files: README.md
      - gitkeep: True
      - parent:
      - children: *edit_subdir_data
    - ref_dir:
      - name: Reference
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children:
    - proj_files_dir:
      - name: Project_Files
      - type: directory
      - path:
      - env:
      - h_env:
      - files: README.md
      - gitkeep: True
      - parent:
      - children: *post_app_subdir_data
    - nuke_dir:
      - name: Nuke
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children:
    - other_dir:
      - name: Other
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children:
    - export_dir:
      - name: Export
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children:
  pre_pro_subdir_data: &pre_pro_subdir_data
    - concept_art_dir:
      - name: Concept_Art
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children:
    - storyboard_dir:
      - name: Storyboard
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children:
    - color_scripts_dir:
      - name: Color_Scripts
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children:
    - animatic_dir:
      - name: Animatic
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children:
    - reference_dir:
      - name: Reference
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children:
    - Other_dir:
      - name: Other
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children:
  shot_subdir_data:
    - shot_config_dir:
      - name: .config
      - type: directory
      - path:
      - env:
      - h_env:
      - files: README.md
      - gitkeep: True
      - parent:
      - children: *geo_subdir_data
    - geo_dir:
      - name: geo
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children: *geo_subdir_data
    - src_dir:
      - name: src
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children: *src_subdir_data
    - hip_dir:
      - name: hip
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children: 
    - render_dir:
      - name: render
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children:
    - texture_dir:
      - name: texture
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children: *tex_subdir_data
    - blend_dir:
      - name: blend
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children:
    - assets_dir:
      - name: assets
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children: *assets_subdir_data
    - hda_dir:
      - name: HDA
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children:
    - reference_dir:
      - name: reference
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children:
    - research_and_development_dir:
      - name: reserach_and_development
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children: 
    - lookdev_dir:
      - name: lookdev
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children:
    - post_production_dir:
      - name: post_production
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children: *post_pro_subdir_data
    - pre_production_dir:
      - name: pre_production
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children: *pre_pro_subdir_data
    - final_dir:
      - name: final
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children:
    - scripts_dir:
      - name: scripts
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children:
    - clips_dir:
      - name: clips
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children:
    - vex_dir:
      - name: vex
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children:
    - other_dir:
      - name: other
      - type: directory
      - path:
      - env:
      - h_env:
      - files:
      - gitkeep: True
      - parent:
      - children:
  project_root:
    - name: test_project
    - type: directory
    - path:
    - env: PROJECT_ROOT
    - h_env:
    - files: README.md
    - gitkeep: True
    - parent:
    - children:
      - assets_dir:
        - name: assets
        - type: directory
        - path:
        - env: GLOBAL_ASSETS_ROOT
        - h_env:
        - files: README.md
        - gitkeep: True
        - parent:
        - children: *assets_subdir_data
      - hsite_dir:
        - name: hsite
        - type: directory
        - path:
        - env: HSITE_ROOT
        - h_env: HSITE
        - files: README.md
        - gitkeep: True
        - parent:
        - children:
      - packages_dir:
        - name: packages
        - type: directory
        - path:
        - env: GLOBAL_PACKAGES
        - h_env: HOUDINI_PACKAGE_DIR
        - files: README.md
        - gitkeep: True
        - parent:
        - children:
      - pre_pro_dir:
        - name: pre_production
        - type: directory
        - path:
        - env: PRE_PRO
        - h_env:
        - files: README.md
        - gitkeep: True
        - parent:
        - children: *pre_pro_subdir_data
      - post_pro_dir:
        - name: post_production
        - type: directory
        - path:
        - env: POST_PRODUCTION
        - h_env:
        - files: README.md
        - gitkeep: True
        - parent:
        - children: *post_pro_subdir_data
      - shots_dir:
        - name: shots
        - type: directory
        - path:
        - env: SHOTS_ROOT
        - h_env:
        - files: README.md
        - gitkeep: True
        - parent:
        - children:
      - delivery_dir:
        - name: deliverables
        - type: directory
        - path:
        - env: DELIVER
        - h_env:
        - files: README.md
        - gitkeep: True
        - parent:
        - children: 
      - hda_dir:
        - name: HDA
        - type: directory
        - path:
        - env:
        - h_env:
        - files: README.md
        - gitkeep: True
        - parent:
        - children:
      - config_dir:
        - name: .config
        - type: directory
        - path:
        - env:
        - h_env:
        - files: README.md
        - gitkeep: True
        - parent:
        - children:














```